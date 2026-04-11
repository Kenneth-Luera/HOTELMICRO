from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hotels.views import HotelViewSet
from hotels.views import RoomViewSet
from drf_spectacular.views import SpectacularAPIView

router = DefaultRouter()
router.register('hotels', HotelViewSet)
router.register('rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]