from django.urls import re_path
from .views import GatewayView, PublicGatewayView

urlpatterns = [
    # ── Auth (publicas) ────────────────────────────────────
    re_path(r'^api/auth/register/$',
            PublicGatewayView.as_view(), {'service_name': 'auth', 'path': 'api/register/'}),
    re_path(r'^api/auth/login/$',
            PublicGatewayView.as_view(), {'service_name': 'auth', 'path': 'api/login/'}),
    re_path(r'^api/auth/refresh/$',
            PublicGatewayView.as_view(), {'service_name': 'auth', 'path': 'api/refresh/'}),

    # ── Hotels (protegidas) ────────────────────────────────
    re_path(r'^api/hotels/$',
            GatewayView.as_view(), {'service_name': 'hotels', 'path': 'api/hotels/'}),
    re_path(r'^api/hotels/(?P<pk>[^/]+)/$',
            GatewayView.as_view(), {'service_name': 'hotels', 'path': 'api/hotels/'}),

    # ── Rooms (protegidas) ─────────────────────────────────
    re_path(r'^api/rooms/$',
            GatewayView.as_view(), {'service_name': 'hotels', 'path': 'api/rooms/'}),
    re_path(r'^api/rooms/(?P<pk>[^/]+)/$',
            GatewayView.as_view(), {'service_name': 'hotels', 'path': 'api/rooms/'}),

    # ── Booking (protegidas) ───────────────────────────────
    re_path(r'^api/bookings/$',
            GatewayView.as_view(), {'service_name': 'booking', 'path': 'bookings/'}),
    re_path(r'^api/bookings/(?P<pk>[^/]+)/$',
            GatewayView.as_view(), {'service_name': 'booking', 'path': 'bookings/'}),
]