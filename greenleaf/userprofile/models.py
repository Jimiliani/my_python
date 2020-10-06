from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


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

    @staticmethod
    def are_friends(user, friend):
        if Friendship.objects.filter(Q(friend1=user) & Q(friend2=friend) & Q(friend1_agree=True) |
                                     Q(friend1=friend) & Q(friend2=user) & Q(friend2_agree=True)).exists():
            return True
        else:
            return False

    @staticmethod
    def delete_friends(who_delete, whom_is_deleted):
        friendship = Friendship.objects.get(
            friend1__user_id=min(who_delete, whom_is_deleted),
            friend2__user_id=max(who_delete, whom_is_deleted))
        if who_delete < whom_is_deleted:
            friendship.friend1_agree = False
        else:
            friendship.friend2_agree = False
        friendship.save()

    @staticmethod
    def make_friends(who_adds, whom_is_added):
        try:
            friendship = Friendship.objects.get(
                friend1__user_id=min(who_adds, whom_is_added),
                friend2__user_id=max(who_adds, whom_is_added))
            friendship.friend1_agree = True
            friendship.friend2_agree = True
            friendship.save()
        except Friendship.DoesNotExist:
            friend1 = User.objects.get(id=who_adds).profile
            friend2 = User.objects.get(id=whom_is_added).profile
            if who_adds < whom_is_added:
                Friendship.objects.create(friend1=friend1, friend2=friend2, friend1_agree=True)
            else:
                Friendship.objects.create(friend1=friend2, friend2=friend1, friend2_agree=True)


class ProfilePost(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    post_text = models.TextField(max_length=10000)
    publication_date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(Profile, related_name='likes')

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return str(self.author) + ' ' + str(self.publication_date)


class PostComment(models.Model):
    post = models.ForeignKey(ProfilePost, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=5000)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post) + ' post ' + str(self.owner) + ' comment owner '


class Message(models.Model):
    dialog = models.ForeignKey(Friendship, on_delete=models.CASCADE, related_name='messages')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(max_length=10000)
    publication_date = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner) + ' ' + str(self.publication_date)
