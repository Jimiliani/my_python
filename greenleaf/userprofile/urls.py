from django.urls import path
from .views import profileViewWithId

app_name = 'userprofile'

urlpatterns = [
    path('user/<int:userId>', profileViewWithId, name='profile'),
]
