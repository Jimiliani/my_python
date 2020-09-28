from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(default='/pictures/default.png', upload_to='pictures/', blank=True)
    city = models.CharField(max_length=63, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    friends = models.ManyToManyField('self', through='Friendship')

    def __str__(self):
        return self.user.__str__()


# пользователь с меньшим id всегда будет friend1, с большим -- friend2
class Friendship(models.Model):
    friend1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend2')
    friend1_agree = models.BooleanField(default=False)
    friend2_agree = models.BooleanField(default=False)

    def __str__(self):
        return str(self.friend1) + ' ' + str(self.friend1_agree) + ' ' \
               + str(self.friend2) + ' ' + str(self.friend2_agree)


class ProfilePost(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    post_text = models.TextField(max_length=10000)
    publication_date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(Profile, related_name='like')

    class Meta:
        ordering = ['-publication_date']

    def serialize_extra_posts(self, user_profile):
        return {
            'id': self.id,
            'post_text': self.post_text,
            'publication_date': self.publication_date,
            'is_liked_by_user': (user_profile in self.like.all()),
            'like_count': self.like.count()
        }


class PostComment(models.Model):
    related_post = models.ForeignKey(ProfilePost, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(max_length=5000)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.related_post) + ' post ' + str(self.owner) + ' comment owner '


class Message(models.Model):
    dialog = models.ForeignKey(Friendship, on_delete=models.CASCADE)
    text = models.TextField(max_length=10000)
    publication_date = models.DateTimeField(auto_now_add=True)
