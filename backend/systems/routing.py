from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/solana/', consumers.SolanaConsumer.as_asgi()),
]