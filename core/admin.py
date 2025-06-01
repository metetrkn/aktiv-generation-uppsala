from django.contrib import admin
from .models import Organization, Activity

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'city', 'updated_at')
    search_fields = ('name', 'email', 'phone', 'city')
    list_filter = ('city', 'country')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone', 'description')
        }),
        ('Address', {
            'fields': ('street', 'city', 'country', 'postal_code')
        }),
        ('Social Media', {
            'fields': ('url', 'youtube', 'facebook', 'instagram')
        }),
        ('Media', {
            'fields': ('logo',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Activity Information', {
            'fields': ('title', 'description', 'date', 'time', 'location')
        }),
        ('Details', {
            'fields': ('max_participants', 'is_active', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ) 