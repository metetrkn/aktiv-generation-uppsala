"""
Common Django settings shared by both production and development environments
"""
from pathlib import Path
import os
from dotenv import load_dotenv


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# Static files (collected by collectstatic), Local fallbacks
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
STATICFILES_DIRS = [BASE_DIR / "static"]

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in environment variables")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core.apps.CoreConfig',
    'apps.mail.apps.MailConfig',
    'apps.photo.apps.PhotoConfig',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'configuration.urls'
WSGI_APPLICATION = 'configuration.wsgi.application'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.organization_info',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {'client_encoding': 'UTF8'}
    }
}

# Password validation (keep as is)
AUTH_PASSWORD_VALIDATORS = [ ... ]

# Internationalization
LANGUAGE_CODE = 'sv'
TIME_ZONE = 'Europe/Stockholm'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    }
}

# S3 shared config (used in prod)
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_QUERYSTRING_AUTH = os.environ.get("AWS_QUERYSTRING_AUTH")

AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=31536000, public",
}
