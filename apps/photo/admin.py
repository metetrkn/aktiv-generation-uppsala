from django.contrib import admin
from .models import Photo

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
