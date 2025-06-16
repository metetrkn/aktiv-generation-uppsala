"""
Core Application Context Processors.

This module contains context processors that add data to the template context
for all templates in the project. The context processors are responsible for:
- Adding organization information to all templates
- Providing global template variables
- Making common data available throughout the application

These processors ensure that important data is consistently available
across all templates without having to pass it explicitly in each view.
"""

from django.conf import settings

def organization_info(request):
    """Add organization information to the template context."""
    return {
        'ORG_NAME': settings.ORG_NAME,
        'ORG_EMAIL': settings.ORG_EMAIL,
        'ORG_PHONE': settings.ORG_PHONE,
        'ORG_STREET': settings.ORG_STREET,
        'ORG_CITY': settings.ORG_CITY,
        'ORG_COUNTRY': settings.ORG_COUNTRY,
        'ORG_POSTAL_CODE': settings.ORG_POSTAL_CODE,
        'ORG_URL': settings.ORG_URL,
        'ORG_DESCRIPTION': settings.ORG_DESCRIPTION,
        'ORG_YOUTUBE': settings.ORG_YOUTUBE,
        'ORG_FACEBOOK': settings.ORG_FACEBOOK,
        'ORG_INSTAGRAM': settings.ORG_INSTAGRAM,
    } 