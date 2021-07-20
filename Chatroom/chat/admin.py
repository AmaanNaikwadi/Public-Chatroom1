from django.contrib import admin
from .models import Thread, Profile, GroupThread, Group, GroupMember

admin.site.register(Profile)
admin.site.register(Thread)
admin.site.register(GroupThread)
admin.site.register(Group)
admin.site.register(GroupMember)