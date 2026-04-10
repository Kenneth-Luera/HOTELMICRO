import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Seguridad ──────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']  # Ajustar en producción

# ── Aplicaciones ───────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'core',
]

# ── Middleware ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# ── URLs ───────────────────────────────────────────────────
ROOT_URLCONF = 'gateway.urls'

# ── Base de datos ──────────────────────────────────────────
# El gateway NO tiene DB propia, valida JWT con la SECRET_KEY
DATABASES = {}

# ── DRF + JWT ──────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.authentication.CustomJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# ── Microservicios ─────────────────────────────────────────
# Nombres de host = nombres de servicio en docker-compose
MICROSERVICES = {
    'auth':    'http://auth_service:8001',
    'hotels':  'http://hotel_service:8000',
    'booking': 'http://booking_service:8002',
    'chat':    'http://chat_service:8004',
}

# ── Internacionalización ───────────────────────────────────
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# ── WSGI ───────────────────────────────────────────────────
WSGI_APPLICATION = 'gateway.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'