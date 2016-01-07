import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here... do not use this UserProfile...user Profile Model
class UserProfile(models.Model):
    #foreign key to tie this info to the user
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=128)
    key_expires = models.DateTimeField(null=True)
    #used to track language preference when we implement it
    locale = models.CharField(max_length=10, null= True)
    #Holds a profile picture on our site
    profile_picture = models.CharField(max_length=256, null=True)
    # Holds their current position e.g. faculty, student, data analyst
    current_title = models.CharField(max_length=100, null=True)
    #This holds the users publicly shared email, after all they may not want to publicise their personal emailmodels
    public_email = models.CharField(max_length=256, null=True)
    #Holds the user set banner picture
    banner_picture = models.CharField(max_length=256, null=True)
    #holds tagline
    tagline=models.CharField(max_length=100, null=True)
    #phoneNumber
    phone = models.CharField(max_length=30, null=True)


    def __str__(self):
        return self.user.email

