from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env file first
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Now import base settings
from .base import *

DEBUG = True


ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Database
DATABASES['default'].update({
    'NAME': os.environ.get('DB_NAME_DEV', 'postgres'),
    'USER': os.environ.get('DB_USER_DEV', 'postgres'),
    'PASSWORD': os.environ.get('DB_PASSWORD_DEV', 'postgres'),
    'HOST': os.environ.get('DB_HOST_DEV', 'localhost'),
    'PORT': os.environ.get('DB_PORT_DEV', '5432'),
    'OPTIONS': {'sslmode': 'disable'}
})

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable security features for development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
