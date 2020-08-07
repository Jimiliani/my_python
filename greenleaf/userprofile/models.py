from django.contrib.auth.models import User
from django.db import models


class GreenLeafUserProfile(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    profile_picture = models.ImageField(default='/pictures/default.png', upload_to='pictures')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=63, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return str(self.user) + ' profile'


class PostProfile(models.Model):
    author = models.ForeignKey(GreenLeafUserProfile, on_delete=models.CASCADE)
    post_text = models.TextField(max_length=5000)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author) + ' post owner ' + str(self.publication_date) + ' publication date'


class PostLike(models.Model):
    related_post = models.ForeignKey(PostProfile, on_delete=models.CASCADE)
    owner = models.ForeignKey(GreenLeafUserProfile, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.related_post) + ' post ' + str(self.owner) + ' like owner '


class PostComment(models.Model):
    related_post = models.ForeignKey(PostProfile, on_delete=models.CASCADE)
    owner = models.ForeignKey(GreenLeafUserProfile, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=1000)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.related_post) + ' post ' + str(self.owner) + ' comment owner '
