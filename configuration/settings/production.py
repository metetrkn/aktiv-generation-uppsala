from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DATABASES['default']['NAME'] = os.environ.get('DB_NAME_PROD', 'aktiv_generation')
DATABASES['default']['USER'] = os.environ.get('DB_USER_PROD', 'postgres')
DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD_PROD', 'bjk123394')
DATABASES['default']['HOST'] = os.environ.get('DB_HOST_PROD', 'localhost')
DATABASES['default']['PORT'] = os.environ.get('DB_PORT_PROD', '5432')
DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}