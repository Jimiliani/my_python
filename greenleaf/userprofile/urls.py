from django.urls import path
from .views import *

app_name = 'userprofile'

urlpatterns = [
    path('logout/', logoutView, name='logout'),
    path('login/', loginView, name='login'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<str:user_id>', ProfileViewWithPk.as_view(), name='profile'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('messages/', messagesView, name='messages'),
    path('dialog/<str:friend_id>', dialogView, name='dialog'),
]
