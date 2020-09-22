from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from userprofile.models import Profile, Friendship


@receiver(post_save, sender=User)
def create_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Friendship)
def create_profile(instance, created, **kwargs):
    if not instance.friend1_agree and not instance.friend2_agree:
        instance.delete()
