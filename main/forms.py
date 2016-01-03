from django import forms
from django.contrib.auth.models import User
from django.core import validators


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # email = forms.charField(validators=[validators.EmailValidator, is_valid_username])

    class Meta:
        model = User

        fields = ('first_name', 'last_name', 'email', 'password')


    def is_valid_username(self, field_data, all_data):
        try:
            User.objects.get(email=field_data)
        except User.DoesNotExist:
            return True
        else:
            raise validators.ValidationError('The email "%s" already exists.'%field_data)

    def save(self, new_data):
        u = User.objects.create(username=new_data['email'], password=new_data['password'],
                                first_name=new_data['first_name'], last_name=new_data['last_name'])
        u.is_active = False
        u.is_staff = False
        u.is_superuser = False
        u.save()
        return u

