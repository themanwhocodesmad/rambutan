import os
from datetime import timedelta
import redis
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-x)w-0d1&ypkzlnsfbjeq%$o86k^n*5-n^4!m5^%##0r-a_@bud'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Auth Applications
    'django.contrib.sites',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',

    # CSS
    'bootstrap4',
    'widget_tweaks',
    'crispy_forms',

    # Knox & DRF
    'rest_framework',
    'knox',
    'corsheaders',

    # Applications
    'users',
    'game_engine',
    'core',

    # Celery Redis
    'django_celery_beat',
    'django_celery_results'

]
SITE_ID = 1  # Use the primary key of your Site instance

CRISPY_TEMPLATE_PACK = 'bootstrap4'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
REST_KNOX = {
    'TOKEN_HEADER_PREFIX': 'Token',
    'TOKEN_TTL': timedelta(hours=168),  # 7 day session time
    'TOKEN_LENGTH': 8  # limit token length to 8 characters
}

MIDDLEWARE = [
    'rambutan.middleware.print_request_middleware.PrintRequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rambutan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rambutan.wsgi.application'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'ca2Bf4D-GDaAFGBEg*1DeAD-g1eBc4Fd',
        'HOST': 'monorail.proxy.rlwy.net',
        'PORT': '22764',
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# CORS_ALLOWED_ORIGINS = [
#     'http://192.168.133.158:8000'
# ]
# CSRF_TRUSTED_ORIGINS = [
#     'http://192.168.133.158:8000'
# ]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
CSRF_TRUSTED_ORIGINS = ['https://orion-test.up.railway.app']
CORS_ALLOWED_ORIGINS = ['https://orion-test.up.railway.app']
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
# Connect to Redis database

# Use the environment variables provided by Railway.app for Redis configuration
REDIS_HOST = 'monorail.proxy.rlwy.net'
REDIS_PORT = '27421'
REDIS_PASSWORD = 'kcGiP4bIKnGPdPopMBL131GGA3gHkN6o'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        }
    }
}

# Celery settings
CELERY_BROKER_URL = 'redis://default:kcGiP4bIKnGPdPopMBL131GGA3gHkN6o@monorail.proxy.rlwy.net:27421'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Johannesburg'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
