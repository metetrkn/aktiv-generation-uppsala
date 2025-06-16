"""
Mail Application URL Configuration.

This module defines the URL patterns for the mail application, including:
- Email template URLs
- Email sending endpoints
- Email tracking URLs
- Mail-related form URLs

The URL patterns are organized to provide a clean and maintainable routing structure
for all mail-related functionality in the application.
"""

from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('', views.mail_us, name='mail_us'),
    path('reply/<int:message_id>/', views.mail_reply, name='mail_reply'),
] 