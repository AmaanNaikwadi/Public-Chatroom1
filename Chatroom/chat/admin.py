from django.contrib import admin
from .models import Thread, Profile, Group, GroupMember, Notification, GroupMessage, ThreadMessage

admin.site.register(Profile)
admin.site.register(Thread)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Notification)
admin.site.register(GroupMessage)
admin.site.register(ThreadMessage)