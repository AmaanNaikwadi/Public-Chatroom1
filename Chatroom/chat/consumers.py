from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User, auth
from chat.models import Thread, Group, GroupMember, Notification, GroupMessage, ThreadMessage
from datetime import datetime, timedelta
import json
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        me = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = User.objects.get(username=other_username)

        try:
            thread = Thread.objects.get(user1=me.username, user2=other_username)
        except Thread.DoesNotExist:
            try:
                thread = Thread.objects.get(user1=other_username, user2=me.username)
            except Thread.DoesNotExist:
                thread = Thread(user1=me.username, user2=other_username)
                thread.save()

        try:
            notification = Notification.objects.get(user=me, sender=other_user)
            notification.read = 0
            notification.save()
        except Notification.DoesNotExist:
            pass

        self.room_name = str(thread.id)
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json['username']
        message = text_data_json['message']
        image = text_data_json['image']
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        me = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = User.objects.get(username=other_username)

        try:
            thread = Thread.objects.get(user1=me.username, user2=other_username)
        except Thread.DoesNotExist:
            thread = Thread.objects.get(user1=other_username, user2=me.username)

        thread_message = ThreadMessage(thread=thread, sender=username, message=str(message)+" ("+str(current_time)+")", image=image, time=current_time)
        thread_message.save()

        if len(self.channel_layer.groups.get(self.room_group_name, {}).items()) == 1:
            try:
                notification = Notification.objects.get(user=other_user, sender=me.username)
                notification.read = 1
                notification.save()
            except Notification.DoesNotExist:
                notification = Notification(user=other_user, sender=me.username, read=1)
                notification.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'personal_message',
                'message': message,
                'username': username,
                'time': str(current_time),
                'number_people': len(self.channel_layer.groups.get(self.room_group_name, {}).items()),
                'image': image,
            }
        )

    async def personal_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']
        number_people = event['number_people']
        image = event['image']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time,
            'number_people': number_people,
            'image': image,
        }))


class GroupChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        group = Group.objects.get(group_name=self.room_name)
        me = self.scope['user']

        group_member = GroupMember.objects.get(user=me, group=group)
        group_member.last_active_time = datetime.now()
        group_member.save()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        image = text_data_json['image']
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        group = Group.objects.get(group_name=self.room_name)
        sender = User.objects.get(username=username)
        gmessage = GroupMessage(group=group, sender=sender, message=str(message)+" ("+str(current_time)+")", time=current_time, image=image)
        gmessage.save()

        group = Group.objects.get(group_name=self.room_name)
        group.last_message_time = datetime.now()
        group.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'group_message',
                'message': message,
                'username': username,
                'time': str(current_time),
                'image': image,
            }
        )

    async def group_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']
        image = event['image']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time,
            'image': image,
        }))


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = 'room'
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        gthread = GroupThread.objects.get(name=self.room_name)
        gthread.chat += str(username) + ' : ' + str(message) + '\n'
        gthread.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))