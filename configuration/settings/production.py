from .base import *
import os

DEBUG = False

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

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Additional production-only apps
INSTALLED_APPS.extend([
    # Any production-specific apps
])

# Production logging
LOGGING['handlers']['file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': '/var/log/django/app.log',
}
LOGGING['root']['handlers'].append('file')