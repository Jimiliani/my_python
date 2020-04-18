from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('<int:pk>/', MainpageView.as_view(), name='mainpage'),
    path('<int:pk>/friends/', FriendsView.as_view(), name='friends'),
]
