from django.contrib import admin
from .models import Photo
from django import forms
from django.utils.safestring import mark_safe

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Photo model.
    
    This class customizes how photos are displayed and managed in the Django admin interface.
    It provides features like filtering, searching, and date-based navigation.
    """
    # Fields to display in the list view
    list_display = ('title', 'uploaded_at')
    
    # Enable filtering by upload date
    list_filter = ('uploaded_at',)
    
    # Enable searching by title and description
    search_fields = ('title', 'description')
    
    # Add date-based navigation in the admin interface
    date_hierarchy = 'uploaded_at'

    # Define the fields to be displayed in the change form, including the image preview
    readonly_fields = ('image_preview',)

    # Define the layout of the change form
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'image_preview', 'description', 'url_path', 'uploaded_at')
        }),
    )

    def image_preview(self, obj):
        """Displays a preview of the image in the admin."""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="auto" />')
        return "No Image"
    image_preview.short_description = 'Preview'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_delete'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        return super().add_view(request, form_url, extra_context=extra_context)

    class PhotoForm(forms.ModelForm):
        class Meta:
            model = Photo
            fields = '__all__'
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not self.instance.pk:
                self.fields['url_path'].initial = 'core/images/'

    form = PhotoForm