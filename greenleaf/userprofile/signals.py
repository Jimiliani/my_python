from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from userprofile.models import Profile


@receiver(post_save, sender=User)
def create_profile(instance, **kwargs):
    Profile.objects.create(user=instance)
    print('Profile created')