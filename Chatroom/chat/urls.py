from django.urls import path, include
from . import views

urlpatterns = [path('', views.signup, name='signup'),
               path('logout', views.logout, name='logout'),
               path('SignIn/', views.signin, name='signin'),
               path('username_validation/', views.username_validation, name='username_validation'),
               path('edit/', views.edit, name='edit'),
               path('Home/', views.home, name='home'),
               path('Home/<str:room_name>/', views.room, name='room'),
               ]