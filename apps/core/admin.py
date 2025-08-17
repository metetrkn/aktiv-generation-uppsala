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

from .models import Activity, ActivityImage


class ActivityImageInline(admin.TabularInline):
    model = ActivityImage
    extra = 1

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
        ("Details", {"fields": ("max_participants", "future_event")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    inlines = [ActivityImageInline]

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_continue"] = False
        extra_context["show_save_and_add_another"] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        return super().add_view(request, form_url, extra_context=extra_context)
