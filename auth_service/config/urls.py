from django.contrib import admin
from django.urls import path
from users.views import RegisterView
from rest_framework_simplejwt.views import  TokenRefreshView
from users.views import CustomTokenView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', RegisterView.as_view()),
    path('api/login/', CustomTokenView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),
]