from django.urls import path
from .views import *

app_name = 'userprofile'

urlpatterns = [
    path('logout/', logoutView, name='logout'),
    path('login/', loginView, name='login'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<int:userId>', profileViewWithId, name='profile'),
]
