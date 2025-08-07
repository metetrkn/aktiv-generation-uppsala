from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"