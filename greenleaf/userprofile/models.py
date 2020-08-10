from django.contrib.auth.models import User
from django.db import models


class GreenLeafUserProfile(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    profile_picture = models.ImageField(default='/pictures/default.png', upload_to='pictures')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=63, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def friends(self):
        return Friendship.objects.filter(owner=User.objects.get(id=self.id))

    def in_friends(self, user):
        if len(Friendship.objects.filter(owner=User.objects.get(id=self.id),
                                         friend=user)) > 0:
            return True
        return False

    def add_friend(self, user):
        this_user = User.objects.get(id=self.id)
        Friendship.objects.create(owner=this_user, friend=user)
        Friendship.objects.create(owner=user, friend=this_user)

    def __str__(self):
        return str(self.user) + ' profile'

    def get_full_name(self):
        return str(self.user.first_name + ' ' + self.user.last_name)


class Friendship(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')

    def __str__(self):
        return str(self.owner) + ' has friend ' + str(self.friend)


class PostProfile(models.Model):
    author = models.ForeignKey(GreenLeafUserProfile, on_delete=models.CASCADE)
    post_text = models.TextField(max_length=5000)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author) + ' post owner ' + str(self.publication_date) + ' publication date'


class PostLike(models.Model):
    post = models.ForeignKey(PostProfile, on_delete=models.CASCADE)
    owner = models.ForeignKey(GreenLeafUserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post.id) + ' post id ' + str(self.owner) + ' like owner '


class PostComment(models.Model):
    related_post = models.ForeignKey(PostProfile, on_delete=models.CASCADE)
    owner = models.ForeignKey(GreenLeafUserProfile, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=1000)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.related_post) + ' post ' + str(self.owner) + ' comment owner '
