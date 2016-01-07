from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
# Model for account recovery
class Recovery(models.Model):
    #foreign key to tie this info to the user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recovery_key = models.CharField(max_length=128)
    key_expires = models.DateTimeField(null=True)
    password = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.user.email


# Model for account activation
class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=128)
    key_expires = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.email

