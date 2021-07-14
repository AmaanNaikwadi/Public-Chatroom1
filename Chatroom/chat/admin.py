from django.contrib import admin
from .models import Thread, Profile

admin.site.register(Profile)
admin.site.register(Thread)