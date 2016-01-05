import uuid, hashlib, datetime

from django.shortcuts import render, HttpResponseRedirect
from django.utils import timezone, html
from django.conf import settings
from django.db.models import Q
from django.core import mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from main import utility
from main.models import User, UserProfile
from account.models import Recovery


# Create your views here.
def recover(request):
    site_url = utility.get_site_url(request)
    valid = False
    error_message = []
    message_type = 'info'
    email = ''
    user = None
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        error_message = [u'You are logged in as {0:s}. If you want to recover another account, please '
                         u'<a href="/logout/">Logout</a> first.'.format(html.escape(request.user.email))]
        valid = False
    # If it's a HTTP POST, we're interested in processing form data.
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        if not email:
            error_message = [u'You must fill in account email address.']
            valid = False
        else:
            # check if username and email exist in database
            user_set = list(User.objects.filter(Q(username=email) | Q(email=email))[:1])
            if user_set:
                valid = True
                user = user_set[0]
            else:
                error_message = [u'Account with email {0:s} does not exist. <a href="/signup/">'
                                 u'Sign up for a new account?</a>'.format(html.escape(email))]
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
        link = "%s/account/reset_password/%s/" % (site_url, recovery_key)
        subject = "Requested password reset"
        txt_message = u'''Hey there,

                    To reset your password, please copy/paste and load the following
                    link to your browser and follow the instruction.

                    Please note that reset link will expire in 48 hours.
                    If you didn't issue a password reset, you cansafely ignore this email.

                    {0:s}

                    Best,
                    Knoect Account Team
                    '''.format(link)
        html_message = u'''Hey there, <br /><br />

                    To reset your {0:s} account password, click on the following link.<br /><br />

                    Please note that reset link will expire in 48 hours.
                    If you didn't issue a password reset, you can safely ignore this email.<br /><br />

                    {1:s}
                    <br /><br />
                    Best,<br />
                    Knoect Account Team
                    '''.format(settings.BRAND_NAME, link)
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        msg = mail.EmailMultiAlternatives(subject, txt_message, from_email, to_list)
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        message = u'''You'll shortly receive your password reset link in
                    {0:s}. Please follow the instruction provided in
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
        recovery_set = list(Recovery.objects.filter(recovery_key=key).order_by('-key_expires')[:1])
        if not recovery_set:
            error_message = u'''The password reset code is not valid. You may request
                        a new activation link to reset your password.
                      '''
            return render(request,
                          'account/recover.html',
                          dict(site_url=site_url, error_message=error_message, email=''))
        else:
            recovery = recovery_set[0]
            user = recovery.user
            # check if this activation link has been already used to set password
            if recovery.password:
                error_message = u'''The password reset code is not valid. You may request
                        a new activation link to reset your password.
                      '''
                return render(request,
                              'account/recover.html',
                              dict(site_url=site_url, error_message=error_message, email=''))
            else:
                if timezone.now() > recovery.key_expires:
                    error_message = u'''The password reset code is not valid. You may request
                        a new activation link to reset your password.
                      '''
                    return render(request,
                                  'account/recover.html',
                                  dict(site_url=site_url, error_message=error_message, email=''))
                    # else:
                    #    success = True

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
                        href="/login/">Log In</a> to your account.
                        '''
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
