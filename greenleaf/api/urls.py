from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('post-list/', PostList.as_view(), name='post-list'),
    path('post-list/<int:user_id>', PostListWithUserId.as_view(), name='user-post-list'),
]
