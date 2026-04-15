# asgi.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_service.settings')
django.setup()  # 👈 esto debe ir ANTES de cualquier import de modelos/consumers

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
from chat.middleware import JWTAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})