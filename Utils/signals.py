from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
import os

@receiver(pre_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    user_profiles = instance.userprofile_set.all()
    for user_profile in user_profiles:
        if user_profile.profile_picture.name != 'no_photo.jpg':
            if os.path.isfile(user_profile.profile_picture.path):
                os.remove(user_profile.profile_picture.path)
