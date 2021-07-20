from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [path('', views.signup, name='signup'),
               path('logout', views.logout, name='logout'),
               path('SignIn/', views.signin, name='signin'),
               path('username_validation/', views.username_validation, name='username_validation'),
               path('edit/', views.edit, name='edit'),
               path('Home/', views.home, name='home'),
               path('Home/<str:room_name>/', views.room, name='room'),
               path('Personal/', views.personal, name='personal'),
               path('Personal/<str:username>/', views.personalchat, name='personalchat'),
               path('Personal/<str:username>/upload/', views.upload, name='upload'),
               path('group/', views.group, name='group'),
               path('groupjoin/', views.groupjoin, name='groupjoin'),
               path('groupjoin/<str:group_name>/', views.groupchat, name='groupchat'),
               path('groupjoin/<str:group_name>/group_upload/', views.group_upload, name='group_upload'),
               path('groupjoin/<str:group_name>/add_member/', views.add_member, name='add_member'),
               path('leave_group/', views.leave_group, name='leave_group'),
               ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)