from django.contrib import admin

# Register your models here.

from main.models import UserProfile

admin.site.register(UserProfile)