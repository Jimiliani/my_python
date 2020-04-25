from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
                  path('', views.home),
                  path('login/', views.login, name='login'),
                  path('logout/', views.logout, name='logout'),
                  path('register/', views.register, name='register'),
                  path('profile/', views.view_profile, name='view_profile'),
                  path('profile/<int:pk>/', views.view_profile, name='view_profile_with_pk'),
                  path('friends/', views.view_friends, name='view_friends'),
                  path('messages/', views.view_messages, name='view_messages'),
                  path('dialog/<int:pk>', views.view_dialog, name='view_dialog_with_pk'),
                  path('connect/<str:operation>/<int:pk>', views.change_friends, name='change_friends'),
                  path('profile/edit/', views.edit_profile, name='edit_profile'),
                  path('change_password/', views.change_password, name='change_password'),
              ]
