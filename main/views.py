import hashlib, uuid, datetime

from django.utils import timezone
from django.shortcuts import render, render_to_response, \
    RequestContext, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.core import mail
from django.conf import settings
from django.core import validators
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import html
from django.template import RequestContext

from main.forms import SignupForm
from main.models import UserProfile
from main import utility
# Create your views here.


def index(request):
    return render_to_response('main/index.html',
                              locals(),
                              context_instance=RequestContext(request))


def user_login(request):
    # print('site = ', request.get_host())
    site_url = utility.get_site_url(request)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        valid = False
        error_message = []
        if not username or not password:
            error_message = ['You must fill in all of the fields']
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # correct password, and the user is marked active
                    auth.login(request, user)
                    request.session['user_id'] = user.id
                    valid = True
                else:
                    error_message = [u'The account is not active. Please request <a class="btn btn-success" ' \
                                     u'href="/activationlink/">New Activation Link</a> to activate your account. Thank you!']
            else:
                error_message = ["Invalid username or password"]

        if valid:
            return HttpResponseRedirect('/profile/')
        else:
            return render(request,
                          'main/login.html',
                          {'site_url': site_url,
                           'error_message': ' '.join(error_message),
                           'username': username,
                           'password': password,
                           })

    else:
        # No context variables to pass to the template system, hence blank
        # dictionary object...
        return render(request, 'main/login.html', {'domain': settings.SITE_URL,})


def signup(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    error_message = []
    site_url = utility.get_site_url(request)
    valid = False
    error_message = []
    message_type = 'info'
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        error_message = [u'You are logged in as {0:s}. If you want to log in to another account, '
                         u'<a class="btn btn-success" href="/logout/">Logout</a> first '
                         u'and re-login.'.format(html.escape(request.user.email))]

        #return render_to_response('main/message.html',
        #                          {'domain': settings.SITE_URL,
        #                           'message_type:': 'info',
        #                           'message': message})

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if not first_name or not last_name or not email or not password:
            error_message = [u'You must fill in all of the fields.']
            return render(request,
                          'main/index.html',
                          {'domain': settings.SITE_URL,
                           'error_message': ' '.join(error_message),
                           'first_name': first_name,
                           'last_name': last_name,
                           'email': email,
                           'password': password,
                           })

        # check for duplicate username and email
        user = User.objects.filter(Q(username=email) | Q(email=email))

        if user:
            error_message = [u'Account with email {0:s} already exists. Please use different email or '
                             'recover your password for the account.'.format(html.escape(email))]
            return render(request,
                          'main/index.html',
                          {'domain': settings.SITE_URL,
                           'error_message': ' '.join(error_message),
                           'first_name': first_name,
                           'last_name': last_name,
                           'email': email,
                           'password': password,
                           })

        try:
            validate_password(password)
        except ValidationError as ex:
            for e in ex:
                error_message.append(e)
            return render(request,
                          'main/index.html',
                          {'domain': settings.SITE_URL,
                           'error_message': ' '.join(error_message),
                           'first_name': first_name,
                           'last_name': last_name,
                           'email': email,
                           'password': password,
                           })

        # Save the user's form data to the database.
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.is_superuser = False
        user.is_staff = False
        # user.set_password(password)
        user.save()
        activation_key = str(uuid.uuid4())
        activation_key = hashlib.sha256(activation_key.encode('utf-8')).hexdigest()
        key_expires = timezone.now() + datetime.timedelta(2)

        # Now sort out the UserProfile instance.
        profile = UserProfile(user=user, activation_key=activation_key,
                              key_expires=key_expires)

        profile.save()
        link = "%s://%s/activate/%s/"%(settings.HTTP_PROTOCOL, settings.SITE_URL, activation_key)
        subject = "Activation link from %s!"%settings.BRAND_NAME

        txt_message = u'''Hey there {0:s},
                    Thank your for your interest. You're off to a great start!

                    To activate your account, please copy and paste this link to your browser and follow the instruction:
                    {2:s}

                    Happy Konecting...

                    Best,
                    Knoect Account Team
                    '''.format(user.first_name, link, link)

        html_message = '''Hey there {0:s}, <br /><br />
                    Thank your for your interest. You're off to a great start!<br />
                    <br>
                    Please click this link <a href="{1:s}" target="_blank">{2:s}</a>
                    to activate your new account.<br /><br />

                    If clicking on the link doesn't work, please copy paste it to
                    your browser. <br /><br />

                    Happy Konecting...<br /><br />

                    Best, <br />
                    Knoect Account Team
                    '''.format(user.first_name, link, link)

        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        msg = mail.EmailMultiAlternatives(subject, txt_message, from_email, to_list)
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        #send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=True)
        # Update our variable to tell the template registration was successful.

        message = u'''New account created successfully. You'll receive your activation link in
                            {0:s}. You must activate you account before you can start Konecting...'''.format(html.escape(user.email))
        return render(request,
                      'main/message.html',
                      {'domain': settings.SITE_URL,
                       'message_type': 'success',
                       'message': message,
                       })
    else:
        return render_to_response('main/signup.html', {'has_account:': False}, RequestContext(request))


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def activate(request, activation_key):
    message = ''
    message_type = 'error'
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        message = u'You are logged in as {0:s}. If you want to activate another account, <a class="btn btn-success" ' \
                  u'href="/logout/">Logout</a> first and click on the link again.'.format(html.escape(request.user.email))
        message_type = 'info'

    #user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    user_profile = list(UserProfile.objects.filter(Q(activation_key=activation_key))[:1])
    if not user_profile:
        message = u'Sorry, but the activation code is invalid. Please request <a class="btn btn-success" '\
                  u'href="/activationlink/">New Activation Link</a> to activate your account. Thank you!'
        message_type = 'error'
    else:
        user = user_profile[0].user
        if user.is_active:
            message = u'Account associated with this activation code is active. You can <a class="btn btn-success" ' \
                      u'href="/login/">Login</a> to your account.'
            message_type = 'info'
        else:
            if timezone.now() < user_profile.key_expires:
                user.is_active = True
                user.save()
                message = u'Thanks for activating your account. You can now <a class="btn btn-success" ' \
                          u'href="/login/">Login</a> to your account.'
                message_type = 'success'
            else:
                message = u'Sorry, but the activation code is expired. Please request <a class="btn btn-success" '\
                          u'href="/activationlink/">New Activation Link</a> to activate your account. Thank you!'
                message_type = 'error'

    return render(request,
                  'main/message.html',
                  {'domain': settings.SITE_URL,
                   'message_type': message_type,
                   'message': message,
                   })


@login_required
def profile(request):
    return render(request, 'main/profile.html', {})

