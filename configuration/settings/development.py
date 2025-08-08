from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
INTERNAL_IPS = ["127.0.0.1"]

# Debug toolbar
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

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

# Debug logging
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers'] = {
    'django': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    },
}