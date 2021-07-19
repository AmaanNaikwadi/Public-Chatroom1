from django.contrib import admin
from .models import Thread, Profile, GroupThread, Message

admin.site.register(Profile)
admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(GroupThread)