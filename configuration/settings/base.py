"""
Common Django settings shared by both production and development environments
"""
from pathlib import Path
import os

# Only load .env in development
if os.getenv("DJANGO_ENV", "development") != "production":
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)

# Project root (aktiv-generation-uppsala)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in environment variables")

# Organization Information
ORG_NAME = os.environ.get('ORG_NAME')
ORG_EMAIL = os.environ.get('ORG_EMAIL')
ORG_PHONE = os.environ.get('ORG_PHONE')
ORG_STREET = os.environ.get('ORG_STREET')
ORG_CITY = os.environ.get('ORG_CITY')
ORG_COUNTRY = os.environ.get('ORG_COUNTRY')
ORG_POSTAL_CODE = os.environ.get('ORG_POSTAL_CODE')
ORG_URL = os.environ.get('ORG_URL')
ORG_DESCRIPTION = os.environ.get('ORG_DESCRIPTION', 'A non-profit organization')
ORG_YOUTUBE = os.environ.get('ORG_YOUTUBE')
ORG_FACEBOOK = os.environ.get('ORG_FACEBOOK')
ORG_INSTAGRAM = os.environ.get('ORG_INSTAGRAM')

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
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Templates, WSGI, URLs (keep all as is)
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

# Database (basic config only)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {'client_encoding': 'UTF8'}
    }
}

# Password validation (keep as is)
AUTH_PASSWORD_VALIDATORS = [ ... ]

# Internationalization (keep as is)
LANGUAGE_CODE = 'sv'
TIME_ZONE = 'Europe/Stockholm'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static and media files (keep as is)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'apps' / 'core' / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging (basic config)
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