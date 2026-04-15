from django.contrib import admin
from django.urls import path
from users.views import RegisterView, UserListView
from rest_framework_simplejwt.views import  TokenRefreshView
from users.views import CustomTokenView
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/register/', RegisterView.as_view()),
    path('api/login/', CustomTokenView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),
    path('api/users/', UserListView.as_view()),
]