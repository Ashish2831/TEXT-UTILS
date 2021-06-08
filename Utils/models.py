from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class UserProfile(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to="Profile_Pictures/", default="no_photo.jpg", blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=50, blank=True)
    university = models.CharField(max_length=50, blank=True)
    about_me = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.user_id)

    def delete(self, *args, **kwargs):
        if self.profile_picture.name != 'no_photo.jpg':
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
                super(UserProfile, self).delete(*args, **kwargs)

class Contacts(models.Model):
    class Meta:
        verbose_name_plural = 'Contacts'

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=50)
    message = models.CharField(max_length=50)
    date = models.DateTimeField(null=True)

class Feature(models.Model):
    image = models.FileField()
    alt = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    url = models.CharField(max_length=50)