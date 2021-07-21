from django.contrib import admin
from .models import Thread, Profile, GroupThread, Group, GroupMember, Notification

admin.site.register(Profile)
admin.site.register(Thread)
admin.site.register(GroupThread)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Notification)