"""
Django settings for configuration project.

This file contains all the configuration for the Django project, including:
- Security settings (SSL, HSTS, CSRF, etc.)
- Database configuration
- Internationalization settings
- Static and media files configuration
- Email settings
- Logging configuration
- Organization-specific settings

The settings are environment-aware and will automatically adjust based on:
- DEBUG mode (development vs production)
- Environment variables
- Host configuration
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in environment variables")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG')

# List of allowed hosts for the application
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Security Settings for production
if not DEBUG:
    # HTTPS settings
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    
    # Other security settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# Organization Information (used in templates and emails)
ORG_NAME = os.environ.get('ORG_NAME')
ORG_EMAIL = os.environ.get('ORG_EMAIL')
ORG_PHONE = os.environ.get('ORG_PHONE')
ORG_STREET = os.environ.get('ORG_STREET')
ORG_CITY = os.environ.get('ORG_CITY')
ORG_COUNTRY = os.environ.get('ORG_COUNTRY')
ORG_POSTAL_CODE = os.environ.get('ORG_POSTAL_CODE')
ORG_URL = os.environ.get('ORG_URL')
ORG_DESCRIPTION = os.environ.get('ORG_DESCRIPTION')

# Social Media links for the organization
ORG_YOUTUBE = os.environ.get('ORG_YOUTUBE')
ORG_FACEBOOK = os.environ.get('ORG_FACEBOOK')
ORG_INSTAGRAM = os.environ.get('ORG_INSTAGRAM')

# Application definition: list of installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core.apps.CoreConfig',
    'apps.mail.apps.MailConfig',
]

# Middleware configuration: handles security, sessions, localization, etc.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Handles language selection
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration for the project
ROOT_URLCONF = 'configuration.urls'

# Template settings: directories, context processors, etc.
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

# WSGI application entry point
WSGI_APPLICATION = 'configuration.wsgi.application'

# Database configuration: uses environment variables for flexibility
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'CONN_MAX_AGE': 60,  # Connection timeout in seconds
        'OPTIONS': {
            'connect_timeout': 10,  # Connection attempt timeout
            'client_encoding': 'UTF8',  # Set client encoding to UTF-8
        },
        'TEST': {
            'NAME': os.environ.get('TEST_DB_NAME', 'test_db'),
        },
    }
}

# Validate database configuration
required_db_settings = ['DB_ENGINE', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
missing_settings = [setting for setting in required_db_settings if not os.environ.get(setting)]
if missing_settings:
    raise ValueError(f"Missing required database settings: {', '.join(missing_settings)}")

# Database security settings for production
if not DEBUG:
    DATABASES['default']['OPTIONS'].update({
        'sslmode': 'verify-full',  # Strict SSL verification in production
    })
else:
    DATABASES['default']['OPTIONS'].update({
        'sslmode': 'prefer',  # Use SSL if available, but don't require it in development
    })

# Password validation settings
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

# Internationalization settings
LANGUAGE_CODE = 'en-us'  # Default language
TIME_ZONE = 'UTC'  # Default timezone
USE_I18N = True  # Enable internationalization
USE_L10N = True  # Enable localization
USE_TZ = True    # Enable timezone support

# Character encoding settings for all files and responses
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

# Static files (CSS, JavaScript, Images) configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'apps' / 'core' / 'static',
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings for sending emails from the application
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Logging configuration for debugging and monitoring
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
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}