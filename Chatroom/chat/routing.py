from django.urls import re_path
from . import consumers
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    re_path(r'ws/chat/', consumers.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

