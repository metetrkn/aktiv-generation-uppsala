"""
Core Application Admin Configuration.

This module configures the Django admin interface for the core application models.
It defines how the models are displayed and managed in the Django admin site,
including:
- Model registration
- Custom admin classes
- Admin interface customization
- Inline admin configurations

The admin interface is designed to provide an intuitive and efficient way to
manage the core application's data.
"""

from django.contrib import admin

from .models import Activity, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "updated_at")
    search_fields = ("name", "email", "phone", "city")
    list_filter = ("city", "country")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Basic Information", {"fields": ("name", "email", "phone", "description")}),
        ("Address", {"fields": ("street", "city", "country", "postal_code")}),
        ("Social Media", {"fields": ("url", "youtube", "facebook", "instagram")}),
        ("Media", {"fields": ("logo",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "time", "location", "future_event")
    list_filter = ("future_event", "date")
    search_fields = ("title", "description", "location")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Activity Information",
            {"fields": ("title", "description", "date", "time", "location")},
        ),
        ("Details", {"fields": ("max_participants", "future_event", "image")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
