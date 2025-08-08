from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DATABASES['default']['NAME'] = os.environ.get('DB_NAME_DEV', 'postgres')
DATABASES['default']['USER'] = os.environ.get('DB_USER_DEV', 'postgres')
DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD_DEV', 'postgres')
DATABASES['default']['HOST'] = os.environ.get('DB_HOST_DEV', 'localhost')
DATABASES['default']['PORT'] = os.environ.get('DB_PORT_DEV', '5432')
DATABASES['default']['OPTIONS'] = {'sslmode': 'disable'}
