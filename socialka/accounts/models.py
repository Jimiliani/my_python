from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, null=True, blank=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.remove(new_friend)


class Dialog(models.Model):
    message_from_id = models.IntegerField()
    message_to_id = models.IntegerField()
    message_text = models.TextField(blank=False)
    sending_time = models.DateTimeField(auto_now_add=True)

    def get_message_from_user(self):
        return User.objects.get(id=self.message_from_id)


class SocialPost(models.Model):
    user_id = models.IntegerField()
    post_text = models.TextField(blank=False)
    sending_time = models.DateTimeField(auto_now=True)

    def get_user_from_user_id(self):
        return User.objects.get(id=self.user_id)
