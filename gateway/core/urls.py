from django.urls import re_path
from .views import GatewayView, PublicGatewayView
from django.views.generic import TemplateView
from .schema import UnifiedSchemaView

urlpatterns = [
        # ── Auth (publicas) ────────────────────────────────────
        re_path(r'^api/auth/register/$',
                PublicGatewayView.as_view(), {'service_name': 'auth', 'path': 'api/register/'}),
        re_path(r'^api/auth/login/$',
                PublicGatewayView.as_view(), {'service_name': 'auth', 'path': 'api/login/'}),
        re_path(r'^api/auth/refresh/$',
                PublicGatewayView.as_view(), {'service_name': 'auth', 'path': 'api/refresh/'}),
        re_path(r'^api/users/$',
                GatewayView.as_view(),{'service_name': 'auth', 'path': 'api/users/'}),

        # ── Hotels (protegidas) ────────────────────────────────
        re_path(r'^api/hotels/$',
                GatewayView.as_view(), {'service_name': 'hotels', 'path': 'api/hotels/'}),
        re_path(r'^api/hotels/(?P<pk>[^/]+)/$',
                GatewayView.as_view(), {'service_name': 'hotels', 'path': 'api/hotels/'}),
        # ── Hotels (publicas) ───────────────────────────────────        
        re_path(r'^api/hotels/public/$',
                PublicGatewayView.as_view(),{'service_name': 'hotels', 'path': 'api/hotels/public/'}),

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

        # swagger
        re_path(r'^api/docs/$',
                TemplateView.as_view(template_name='swagger.html'), name='swagger-ui'),
        re_path(r'^api/docs/schema/$',
                UnifiedSchemaView.as_view(), name='unified-schema'),
        # ── Posts (protegidas) ───────────────────────────────
        re_path(r'^api/posts/$',
                GatewayView.as_view(), {'service_name': 'posts', 'path': 'api/posts/'}),

        re_path(r'^api/posts/(?P<pk>[^/]+)/$',
                GatewayView.as_view(), {'service_name': 'posts', 'path': 'api/posts/'}),
]