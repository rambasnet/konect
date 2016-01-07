import uuid, hashlib, datetime
from urllib.parse import urljoin

from django.shortcuts import render, HttpResponseRedirect
from django.utils import timezone, html
from django.conf import settings
from django.db.models import Q
from django.core import mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.contrib.auth import models
from django.core.urlresolvers import reverse

from main import utility
from account.models import Recovery, Activation
from account import messages
from eprofile.models import Profile


# Create your views here.
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
                    url = reverse('account:activation')
                    error_message = [u'''The account is not active. Please check you email for activation link or you may <a
                                     href="{url}">Request New Activation Link</a> to activate your account.
                                     '''.format(url=url)]
            else:
                error_message = ["Invalid username or password"]

        if valid:
            return HttpResponseRedirect('/profile/')
        else:
            return render(request,
                          'account/login.html',
                          {'site_url': site_url,
                           'error_message': ' '.join(error_message),
                           'username': username,
                           'password': password,
                           })

    else:
        # No context variables to pass to the template system, hence blank
        # dictionary object...
        return render(request,
                      'account/login.html',
                      {
                          'site_url': site_url,
                      })


def signup(request):
    site_url = utility.get_site_url(request)
    valid = False
    error_message = []
    message_type = 'info'
    first_name = ''
    last_name = ''
    email = ''
    password = ''
    # path = request.get_full_path()
    # print('path = ', path)
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        error_message = [u'''You are logged in as {username}. If you'd like to register another account,
                         <a href="{url}">Logout</a> first.
                         '''.format(username=html.escape(request.user.username), url=settings.LOGOUT_URL)]
        valid = False
    # If it's a HTTP POST, we're interested in processing form data.
    elif request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if not first_name or not last_name or not email or not password:
            error_message = [u'You must fill in all of the fields.']
            valid = False
        else:
            # check for duplicate username and email
            user = models.User.objects.filter(Q(username=email) | Q(email=email))
            if user:
                url = reverse('account:recover')
                error_message = [u'''Account with email {email} already exists. <a href="{url}">
                                 Forgot your password? </a>
                                 '''.format(email=html.escape(email), url=url)]
                valid = False
            else:
                try:
                    validate_password(password)
                    valid = True
                except ValidationError as ex:
                    valid = False
                    for e in ex:
                        error_message.append(e)
    else:
        return render(request,
                      'account/signup.html',
                      {
                          'site_url': site_url,
                      })

    if valid:
        # Save the user's form data to the database.
        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.is_superuser = False
        user.is_staff = False
        # user.set_password(password)
        user.save()
        card_name = "%s %s"%(user.first_name, user.last_name)
        profile = Profile(user=user, card_name=card_name, card_email=user.email)
        profile.save()
        generate_activation_key_and_send_email(site_url, user)
        # send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=True)
        # Update our variable to tell the template registration was successful.

        error_message = [u'''New account created successfully. You'll receive your activation link in
                    {0:s}. You must activate you account before you can log in...'''
            .format(html.escape(user.email))]

        return render(request,
                      'main/message.html',
                      {
                          'site_url': site_url,
                          'message_type': 'success',
                          'message': ' '.join(error_message),
                      })

    else:
        return render(request,
                      'account/signup.html',
                      {
                          'site_url': site_url,
                          'error_message': ' '.join(error_message),
                          'first_name': first_name,
                          'last_name': last_name,
                          'email': email,
                          'password': password,
                      })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def activate(request, activation_key):
    message = ''
    message_type = 'error'
    site_url = utility.get_site_url(request)

    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        message = u'''You are logged in as {username}. If you want to activate another account,
                    <a href="{url}">Logout</a> first and click on the activation link again.
                    '''.format(url=settings.LOGOUT_URL, username=html.escape(request.user.username))
        message_type = 'info'

    else:  # user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
        acct_set = list(Activation.objects.filter(Q(activation_key=activation_key))[:1])
        activation_url = reverse('account:activation')
        valid = True
        if not acct_set:
            message = u'''The activation code is not valid. You may
                        request new activation link</a> to activate your account.
                        '''.format(url=activation_url)
            valid = False
        else:
            acct = acct_set[0]
            user = acct.user
            if user.is_active:
                message = u'''Account associated with this activation code is active.
                            You may <a href="{url}">Login</a> to your account.
                            '''.format(url=settings.LOGIN_URL)
                message_type = 'info'
                valid = True
            else:
                if timezone.now() < acct.key_expires:
                    user.is_active = True
                    user.save()
                    message = u'''Your account has been activated successfully. You can now <a class="btn btn-success"
                                href="{login}">Login</a> to your account.
                                '''.format(login=settings.LOGIN_URL)
                    message_type = 'success'
                    valid = True
                else:
                    message = u'''The activation link has expired. You may
                                <a class="btn btn-success" href="{activation_link}">Request New Activation Link</a>
                                 to activate your account.
                                 '''.format(activation_url)
                    message_type = 'error'
                    valid = False
    if valid:
        return render(request,
                      'main/message.html',
                      {
                          'site_url': site_url,
                          'message_type': message_type,
                          'message': message,
                      })
    else:
        return render(request,
                      'account/activate.html',
                      dict(site_url=site_url, error_message = message))


def recover(request):
    site_url = utility.get_site_url(request)
    valid = False
    error_message = []
    message_type = 'info'
    email = ''
    user = None
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        error_message = [u'''You are logged in as {username}. If you want to recover another account, please
                         <a href="{logout}">Logout</a> first.
                         '''.format(username=html.escape(request.user.username), logout=settings.LOGOUT_URL)]
        valid = False
    # If it's a HTTP POST, we're interested in processing form data.
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        if not email:
            error_message = [u'You must fill in account email address.']
            valid = False
        else:
            # check if username and email exist in database
            user_set = list(models.User.objects.filter(Q(username=email) | Q(email=email))[:1])
            if user_set:
                valid = True
                user = user_set[0]
            else:
                error_message = [u'''Account with email {username} does not exist.
                                <a href="{signup}"> Sign up for a new account?</a>
                                '''.format(username=html.escape(email))]
                valid = False
    else:
        return render(request,
                      'account/recover.html',
                      {
                          'site_url': site_url,
                      })

    if valid and user:
        # user.set_password(password)
        recovery_key = str(uuid.uuid4())
        recovery_key = hashlib.sha256(recovery_key.encode('utf-8')).hexdigest()
        key_expires = timezone.now() + datetime.timedelta(2)
        # Now sort out the UserProfile instance.
        recovery = Recovery(user=user, recovery_key=recovery_key, key_expires=key_expires)
        recovery.save()
        link = reverse('account:reset_password', args=(recovery_key,))
        subject = "Requested password reset"
        txt_message = u'''Hey there,

                    To reset your password, please copy/paste and load the following
                    link to your browser and follow the instruction.

                    Please note that reset link will expire in 48 hours.
                    If you didn't issue a password reset, you cansafely ignore this email.

                    {link}

                    Best,
                    {brand_name} Account Team
                    '''.format(link=link, brand_name=settings.BRAND_NAME)
        html_message = u'''Hey there, <br /><br />

                    To reset your {brand_name} account password, click on the following link.<br /><br />

                    Please note that reset link will expire in 48 hours.
                    If you didn't issue a password reset, you can safely ignore this email.<br /><br />

                    {link}
                    <br /><br />
                    Best,<br />
                    {brand_name} Account Team
                    '''.format(brand_name=settings.BRAND_NAME, link=link)

        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        msg = mail.EmailMultiAlternatives(subject, txt_message, from_email, to_list)
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        message = u'''You'll shortly receive your password reset link in
                    {0:s}. Please follow the instructions provided in
                    the email to reset your password.'''.format(html.escape(email))
        return render(request,
                      'main/message.html',
                      dict(site_url=site_url, message_type='success', message=message))
    else:
        return render(request,
                      'account/recover.html',
                      dict(site_url=site_url, error_message=' '.join(error_message), email=email))


def validate_passwords(pass1, pass2):
    error_message = []
    if not pass1 or not pass2:
        error_message = ['Both the passwords need to be filled in and matched.']
    elif pass1 != pass2:
        error_message = ['Two passwords do not match.']
    else:
        try:
            validate_password(pass1)
            success = True
        except ValidationError as ex:
            success = False
            for e in ex:
                error_message.append(e)
    return ' '.join(error_message)


def reset_password(request, key=None):
    error_message = ''
    message_type = 'error'
    site_url = utility.get_site_url(request)
    success = False
    user = None
    recovery = None
    if request.user.is_authenticated():
        user= request.user
    else:
        valid = True
        recovery_set = list(Recovery.objects.filter(recovery_key=key).order_by('-key_expires')[:1])
        if not recovery_set:
            error_message = u'''The password reset link is not valid. You may request
                        a new reset link.
                      '''
            valid = False
        else:
            recovery = recovery_set[0]
            user = recovery.user
            # check if this activation link has been already used to set password
            if recovery.password:
                error_message = u'''The password reset code is not valid. You may request
                        a new activation link to reset your password.
                      '''
                valid = False
            else:
                if timezone.now() > recovery.key_expires:
                    error_message = u'''The password reset code is not valid. You may request
                        a new activation link to reset your password.
                      '''
                    valid = False


        if not valid:
            return render(request,
                          'account/recover.html',
                          dict(site_url=site_url, error_message=error_message, email=''))

    if request.method == 'POST':
        pass1 = request.POST.get('password1', '')
        pass2 = request.POST.get('password2', '')
        error_message = validate_passwords(pass1, pass2)
        if not error_message:
            user.set_password(pass1)
            user.save()
            message = u'''Your password has been changed.'''
            # password change for logged in user
            if not request.user.is_authenticated():
                recovery.password = user.password
                recovery.save()

                message = u'''Your password has been changed. You can now <a class="btn btn-success"
                        href="{login}">Log In</a> to your account.
                        '''.format(settings.LOGIN_URL)

            message_type = 'success'
            return render(request,
                          'main/message.html',
                          {
                              'site_url': site_url,
                              'message_type': message_type,
                              'message': message,
                          })
        else:
            return render(request,
                          'account/password.html',
                          {
                              'site_url': site_url,
                              'error_message': error_message,
                              'password1': pass1,
                              'password2': pass2,
                          })
    else:
        return render(request,
                      'account/password.html',
                      dict(site_url=site_url, key=key))


def activation(request):
    site_url = utility.get_site_url(request)
    valid = False
    error_message = []
    message_type = 'info'
    email = ''
    user = None
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        error_message = [u'''You are logged in as {username}. If you want to activate another account, please
                         <a href="{logout}">Logout</a> first.
                         '''.format(username=html.escape(request.user.username), logout=settings.LOGOUT_URL)]
        valid = False
    # If it's a HTTP POST, we're interested in processing form data.
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        if not email:
            error_message = [u'You must fill in account email address.']
            valid = False
        else:
            # check if username and email exist in database
            user_set = list(models.User.objects.filter(Q(username=email) | Q(email=email))[:1])
            if user_set:
                valid = True
                user = user_set[0]
            else:
                error_message = [u'''Account with email {username} does not exist.
                                <a href="{signup}"> Sign up for a new account?</a>
                                '''.format(username=html.escape(email), signup=reverse('account:signup'))]
                valid = False

    if valid and user:
        # user.set_password(password)
        generate_activation_key_and_send_email(site_url, user)
        message = u'''You'll shortly receive your account activation link in
                    {email}. Please follow the instructions provided in
                    the email to reset your password.
                    '''.format(email=html.escape(email))
        return render(request,
                      'main/message.html',
                      dict(site_url=site_url, message_type='success', message=message))
    else:
        return render(request,
                      'account/activate.html',
                      dict(site_url=site_url, error_message=' '.join(error_message), email=email))


def generate_activation_key_and_send_email(site_url, user):
    activation_key = str(uuid.uuid4())
    activation_key = hashlib.sha256(activation_key.encode('utf-8')).hexdigest()
    key_expires = timezone.now() + datetime.timedelta(2)
    act = Activation(user=user, activation_key=activation_key, key_expires=key_expires)
    act.save()
    # link = "%s/activate/%s/" % (site_url, activation_key)
    link = urljoin(site_url, reverse('account:activate', args=(activation_key,)))
    subject = "Activation link from %s!" % settings.BRAND_NAME
    txt_message = messages.txt_activation_msg.format(name=user.first_name, link=link, brand_name=settings.BRAND_NAME)
    html_message = messages.html_activation_msg.format(name=user.first_name, link=link, brand_name=settings.BRAND_NAME)
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email]
    msg = mail.EmailMultiAlternatives(subject, txt_message, from_email, to_list)
    msg.attach_alternative(html_message, "text/html")
    msg.send()
