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


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    message = models.TextField()
    image = models.IntegerField(default=0)
    message_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.now())

    def __str__(self):
        return self.message


class GroupThread(models.Model):

    name = models.CharField(max_length=50)
    chat = models.TextField()

    def __str__(self):
        return self.name