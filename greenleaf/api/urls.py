from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('post-list/', PostList.as_view(), name='post-list'),
    path('post-list/<int:user_id>/', PostListWithUserId.as_view(), name='user-post-list'),
    path('friendship-list/', FriendshipList.as_view(), name='friendship-list'),
    path('friendship-list/<int:friend_id>/', FriendshipListWithFriendId.as_view(), name='friendship-list-with-friend-id'),
    path('like-list/<int:post_id>/', LikeList.as_view(), name='like-list'),
]
