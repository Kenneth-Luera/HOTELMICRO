from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet
from rest_framework.schemas import get_schema_view
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    title="Post API",
    description="API de publicaciones",
    version="1.0.0",
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', schema_view),
    path('api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)