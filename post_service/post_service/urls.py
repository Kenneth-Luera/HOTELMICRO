from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView
from django.conf import settings
from django.conf.urls.static import static
from posts.views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)