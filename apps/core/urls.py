"""
Core Application URL Configuration.

This module defines the URL patterns for the core application, including:
- Main page URLs
- Core functionality URLs
- Any other URLs specific to the core application

The URL patterns are organized to provide a clean and maintainable routing structure
for the core application's views.
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('cookies/', views.cookies, name='cookies'),
] 