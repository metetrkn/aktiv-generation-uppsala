"""
Core Application Configuration.

This module configures the core Django application, which serves as the main
application for the project. It handles the basic configuration of the app,
including its name and any app-specific settings.

The core app is responsible for:
- Basic site functionality
- Organization information
- Common templates and static files
"""

from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core' 