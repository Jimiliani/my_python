from django.urls import path
from .views import profileViewWithId, RegisterView, logoutView, loginView

app_name = 'userprofile'

urlpatterns = [
    path('logout/', logoutView, name='logout'),
    path('login/', loginView, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<int:userId>', profileViewWithId, name='profile'),
]
