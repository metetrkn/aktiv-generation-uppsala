"""
WSGI Configuration for the Django project.

This module exposes the WSGI callable as a module-level variable named 'application'.
It is used by the WSGI server (e.g., Gunicorn, uWSGI) to run the Django application.

The WSGI application is configured to use the project's settings module and
handles the interface between the web server and the Django application.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')

application = get_wsgi_application() 