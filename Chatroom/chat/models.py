from django.db import models
from django.contrib.auth.models import User, auth
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, default=True)

    def __str__(self):
        return self.user.username


class Photo(models.Model):
    img = models.ImageField(null=True, blank=True)


class Thread(models.Model):

    user1 = models.CharField(max_length=50)
    user2 = models.CharField(max_length=50)
    chat = models.TextField()

    def __str__(self):
        return str(self.user1)+" "+str(self.user2)


class GroupThread(models.Model):

    name = models.CharField(max_length=50)
    chat = models.TextField()

    def __str__(self):
        return self.name


class Group(models.Model):
    group_name = models.CharField(max_length=50)
    last_message_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.group_name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_active_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.group.group_name

