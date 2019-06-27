from django.urls import path
from jumpserver.tools.channel import websocket

websocket_urlpatterns = [
    path('webssh/', websocket.WebSSH),
]
