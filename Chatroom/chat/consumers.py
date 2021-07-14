from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User, auth
from chat.models import Thread
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

        me = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = User.objects.get(username=other_username)

        try:
            thread = Thread.objects.get(user1=me.username, user2=other_username)
        except Thread.DoesNotExist:
            thread = Thread.objects.get(user1=other_username, user2=me.username)

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        thread.chat += '(' + str(current_time) + ')' + str(username) + ' : ' + str(message) + '\n'
        thread.save()


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'personal_message',
                'message': message,
                'username': username,
                'time': str(current_time)
            }
        )

    async def personal_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time,
        }))


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = 'chat'
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
