from django.contrib import admin
from .models import Thread, Profile, GroupThread

admin.site.register(Profile)
admin.site.register(Thread)
admin.site.register(GroupThread)