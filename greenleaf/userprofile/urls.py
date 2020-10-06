from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetCompleteView
from django.urls import path
from .views import *

app_name = 'userprofile'

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='userprofile/password_reset.html',
        email_template_name='userprofile/email_message_for_password_change.html',
        success_url='../password_reset_done/'),
         name='password-reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='userprofile/password_reset_done.html'),
         name='password-reset-done'),
    path('password_reset/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(
        template_name='userprofile/password_reset_confirm.html',
        success_url='../../../password_reset_complete/'),
         name='password-reset-confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(
        template_name='userprofile/password_reset_complete.html'), name='password-reset-complete'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<str:user_id>', ProfileViewWithPk.as_view(), name='profile'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('dialog/<str:friend_id>', DialogView.as_view(), name='dialog'),
]
