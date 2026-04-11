from rest_framework.routers import DefaultRouter
from booking.views import BookingViewSet
from drf_spectacular.views import SpectacularAPIView
from django.urls import path

router = DefaultRouter()
router.register('bookings', BookingViewSet, basename='booking')

urlpatterns = router.urls + [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]