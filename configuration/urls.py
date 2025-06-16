"""
URL Configuration for the Django project.

This module defines the URL patterns for the entire project, including:
- Admin interface URLs
- Core application URLs
- Mail application URLs
- Static and media file serving in development

The URL patterns are organized by application and follow Django's URL routing best practices.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "Aktiv Generation Administration"
admin.site.site_title = "Aktiv Generation Admin Portal"
admin.site.index_title = "Welcome to Aktiv Generation Admin Portal"

urlpatterns = [
    path('supadmin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('mejla-oss/', include('apps.mail.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 