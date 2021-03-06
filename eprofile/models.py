import uuid, datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'img/{0}/{1}'.format(instance.user.id, filename)


# Create your models here.
class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, max_length=256, null=False)
    created = models.DateTimeField(default=timezone.now, null=False)
    album = models.CharField(max_length=256, null=False)

    def __str__(self):
        return self.photo.name


# Create your models here.
class Profile(models.Model):
    #foreign key to tie this info to the user
    user = models.OneToOneField(User)
    created = models.DateTimeField(editable=False, null=False)
    modified = models.DateTimeField(null=True)
    #used to track language preference when we implement it
    locale = models.CharField(max_length=10, null= True)
    #Holds a profile picture on our site
    profile_photo = models.CharField(max_length=256, null=True)
    cover_photo = models.CharField(max_length=256, null=True)
    # Holds their current position e.g. faculty, student, data analyst
    card_name = models.CharField(max_length=100, null=True)
    card_title = models.CharField(max_length=100, null=True)
    card_department = models.CharField(max_length=100, null=True)
    card_employer = models.CharField(max_length=100, null=True)
    card_address1 = models.CharField(max_length=256, null=True)
    card_address2= models.CharField(max_length=256, null=True)
    card_email = models.EmailField(max_length=256, null=True)
    card_phone = models.CharField(max_length=30)
    card_office = models.CharField(max_length=100)
    is_verified = models.NullBooleanField()
    summary = models.TextField(null=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        '''
        On save, update timestamps
        '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Profile, self).save(*args, **kwargs)


class Education(models.Model):
    user = models.ForeignKey(Profile)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(null=True, editable=False)
    modified = models.DateTimeField(null=True)
    school = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=256, null=True, blank=True)
    month_from = models.IntegerField( null=True, blank=True)
    month_to = models.IntegerField(null=True, blank=True)
    year_from = models.IntegerField(null=True, blank=True)
    year_to = models.IntegerField(null=True, blank=True)
    graduated = models.NullBooleanField(null=True, blank=True)
    current = models.BooleanField(default=False)
    degree = models.CharField(max_length=20, null=True, blank=True)
    major_field = models.CharField(max_length=20, null=True, blank=True)
    concentrations = models.CharField(max_length=256, blank=True)
    gpa = models.CharField(max_length=10, null=True, blank=True)
    activities = models.TextField(null=True, blank=True)
    societies = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-year_to', '-month_to']

    def __str__(self):
        return self.school

    def save(self, *args, **kwargs):
        '''
        On save, update timestamps
        '''
        if not self.id:
            self.created = timezone.now()
        if self.current:
            self.month_to = datetime.date.today().month
            self.year_to = datetime.date.today().year
        self.modified = timezone.now()
        return super(Education, self).save(*args, **kwargs)


class Experience(models.Model):
    user = models.ForeignKey(Profile)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(null=False, editable=False)
    modified = models.DateTimeField(null=False, editable=False)
    company = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=256, null=True, blank=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    month_from = models.IntegerField(null=False, blank=False)
    year_from = models.IntegerField(null=False, blank=False)
    month_to = models.IntegerField(null=True, blank=True)
    year_to = models.IntegerField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-year_to', '-month_to']

    def __str__(self):
        return self.school

    def save(self, *args, **kwargs):
        '''
        On save, update timestamps
        '''
        if not self.id:
            self.created = timezone.now()
        if self.current:
            self.month_to = datetime.date.today().month
            self.year_to = datetime.date.today().year
        self.modified = timezone.now()
        return super(Experience, self).save(*args, **kwargs)