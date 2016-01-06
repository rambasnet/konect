from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'img/{0}/{1}'.format(instance.user.id, filename)


# Create your models here.
class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, max_length=256, null=False)
    timestamp = models.DateTimeField(default=timezone.now, null=False)
    album = models.CharField(max_length=256, null=False)

    def __str__(self):
        return self.photo.name

