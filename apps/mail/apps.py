"""
Mail Application Configuration.

This module configures the mail Django application, which handles all email-related
functionality in the project. It manages the configuration of the mail app,
including its name and any app-specific settings.

The mail app is responsible for:
- Email template management
- Email sending functionality
- Email tracking and logging
- Mail-related admin interfaces
"""

from django.apps import AppConfig


class MailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.mail"
