"""
URL configuration for configuration project.
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