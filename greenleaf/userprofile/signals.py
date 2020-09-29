from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from userprofile.models import Profile, Friendship


@receiver(post_save, sender=User)
def create_profile(instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()


@receiver(post_save, sender=Friendship)
def delete_friendship(instance, created, **kwargs):
    if not instance.friend1_agree and not instance.friend2_agree:
        instance.delete()
