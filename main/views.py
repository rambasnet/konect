import hashlib, uuid, datetime

from django.shortcuts import render, render_to_response, \
    RequestContext, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
from django.core import validators
from django.db.models import Q
from django.core.exceptions import ValidationError

from main.forms import SignupForm
from main.models import UserProfile
# Create your views here.


def index(request):
    return render_to_response('main/index.html',
                              locals(),
                              context_instance=RequestContext(request))


def user_login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    # correct password, and the user is marked active
                    auth.login(request, user)
                    request.session['member_id'] = user.id
                    return HttpResponseRedirect('/admin/')
                else:
                    return HttpResponse('Account is disabled!')
            else:
                return HttpResponse("Invalid username or password")
        except:
            return HttpResponse("Invalid username or password")
    else:
        # No context variables to pass to the template system, hence blank
        # dictionary object...
        return render(request, 'login.html', {})


def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        return render_to_response('signup.html', {'has_account:': True})

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        user_form = SignupForm(data=request.POST)
        new_data = request.POST.copy()
        errors = user_form.get_validation_errors(new_data)
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        if not errors:

            #profile_form = UserProfileForm(data=request.POST)

            # If the two forms are valid...
            if user_form.is_valid():
                # Save the user's form data to the database.
                user = user_form.save(new_data)
                activation_key = str(uuid.uuid4())
                activation_key = hashlib.sha256(activation_key.encode('utf-8'))
                key_expires = datetime.datetime.today() + datetime.timedelta(2)
                # Now we hash the password with the set_password method.
                # Once hashed, we can update the user object.
                user.set_password(user.password)
                user.save()
                # Now sort out the UserProfile instance.
                # Since we need to set the user attribute ourselves, we set commit=False.
                # This delays saving the model until we're ready to avoid integrity problems.
                profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
                # Did the user provide a profile picture?
                # If so, we need to get it from the input form and put it in the UserProfile model.
                # if 'picture' in request.FILES:
                #    profile.picture = request.FILES['picture']
                #

                link = "%s/activate/"%settings.SITE_URL

                # Now we save the UserProfile model instance.
                profile.save()
                subject = "Activation link from %s!"%settings.BRAND_NAME

                message = '''Dear %s, <br>
                            Thank your for your interest. You're off to a great start!<br>
                            <br>
                            You must click this link <a href="%s" target="_blank">%s</a>
                            to activate your new account.<br>

                            If clicking on the link doesn't work, please copy paste it to
                            a browser's address bar. <br />

                            Happy Konecting...<br />

                            Best, <br />
                            Knoect Account Team
                            '''%(user.first_name, link, link)
                from_email = settings.EMAIL_HOST_USER
                to_list = [user.email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
                # Update our variable to tell the template registration was successful.
                registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = SignupForm()

    # Render the template depending on the context.
    return render(request,
            'signup.html',
            {'user_form': user_form, 'registered': registered})


def signup(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        return render_to_response('signup.html', {'has_account:': True})

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # check for duplicate username and email
        user = User.objects.filter(Q(username=email) | Q(email=email))
        error_message = []
        if user:
            error_message = [u'Account with email {0:s} already exists. Please use different email or ' \
                    u'recover your password for the account.'.format(email)]
            return render(request,
                          'main/index.html',
                          {'error_message': ' '.join(error_message),
                           })

        try:
            validate_password(password)
        except ValidationError as ex:
            for e in ex:
                error_message.append(e)
            return HttpResponse(error_message)

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
        key_expires = datetime.datetime.today() + datetime.timedelta(2)

        # Now sort out the UserProfile instance.
        # Since we need to set the user attribute ourselves, we set commit=False.
        # This delays saving the model until we're ready to avoid integrity problems.
        profile = UserProfile(user=user, activation_key=activation_key,
                              key_expires=key_expires)
        # Did the user provide a profile picture?
        # If so, we need to get it from the input form and put it in the UserProfile model.
        # if 'picture' in request.FILES:
        #    profile.picture = request.FILES['picture']
        #
        # Now we save the UserProfile model instance.
        profile.save()
        link = "%s/activate/"%settings.SITE_URL
        subject = "Activation link from %s!"%settings.BRAND_NAME

        message = u'''Dear {0:s}, <br>
                    Thank your for your interest. You're off to a great start!<br>
                    <br>
                    You must click this link <a href="{1:s}" target="_blank">{2:s}</a>
                    to activate your new account.<br>

                    If clicking on the link doesn't work, please copy paste it to
                    a browser's address bar. <br />

                    Happy Konecting...<br />

                    Best, <br />
                    Knoect Account Team
                    '''.format(user.first_name, link, link)
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        # Update our variable to tell the template registration was successful.
        registered = True
        feedback = u'''New account created successfully. You'll receive an activation link in
                            {0:s}. You must activate you account before you can start Konecting...'''.format(user.email)
        return HttpResponse(feedback)
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        # else:
        #    print(user_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    #else:
    #    user_form = SignupForm()

    # Render the template depending on the context.
    # return render(request,
    #        'register.html',
    #        {'user_form': user_form, 'registered': registered})
    return HttpResponse("Problem signing up user!")


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def activate(request, activation_key):
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        return render_to_response('confirm.html', {'has_account:': True})
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    if user_profile.key_expires < datetime.datetime.today():
        return render_to_response('confirm.html', {'expired':True})
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return render_to_response('confirm.html', {'success': True})
