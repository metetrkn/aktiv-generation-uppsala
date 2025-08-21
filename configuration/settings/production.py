from .base import *
import os

DEBUG = False

# Email system does not crash if email fails to send in production
FAIL_SILENTLY = True

# Security settings
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Database
DATABASES['default'].update({
    'NAME': os.environ.get('DB_NAME_PROD'),
    'USER': os.environ.get('DB_USER_PROD'),
    'PASSWORD': os.environ.get('DB_PASSWORD_PROD'),
    'HOST': os.environ.get('DB_HOST_PROD'),
    'PORT': os.environ.get('DB_PORT_PROD', '5432'),
    'OPTIONS': {'sslmode': 'require'}
})

# Email (SMTP for production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Additional production-only apps
INSTALLED_APPS.extend([
    "storages",
])

# Production logging
LOGGING['handlers']['file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': '/var/log/django/app.log',
}

LOGGING['root']['handlers'].append('file')

# Use custom S3 storages
STATICFILES_STORAGE = "storages_backend.StaticStorage"
DEFAULT_FILE_STORAGE = "storages_backend.MediaStorage"

STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/static/"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/media/"
