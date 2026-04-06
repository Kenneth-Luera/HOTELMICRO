from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hotels.views import HotelViewSet
from hotels.views import RoomViewSet

router = DefaultRouter()
router.register('hotels', HotelViewSet)
router.register('rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('api/', include(router.urls)),
]