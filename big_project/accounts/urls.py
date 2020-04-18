from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'accounts'
urlpatterns = [
    path('me/', mainpage, name='mainpage'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('friends/', friends, name='logout'),
]
