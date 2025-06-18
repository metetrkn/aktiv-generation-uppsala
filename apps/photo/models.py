from django.db import models
from django.utils import timezone
from django.conf import settings
import os
import shutil

class Photo(models.Model):
    """
    Model representing a photo in the system.
    
    This model stores information about photos including their title, image file,
    description, and upload timestamp. Photos are stored in the 'core/images/' directory
    within the media folder.
    """
    title = models.CharField(
        max_length=200,
        help_text="The title or name of the photo"
    )
    image = models.ImageField(
        upload_to='core/images/',
        help_text="The actual image file. Will be stored in core/static/core/images/ directory"
    )
    url_path = models.CharField(
        max_length=255,
        blank=True,
        help_text="The URL path to access the image"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description or additional information about the photo"
    )
    uploaded_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp of when the photo was uploaded"
    )

    def __str__(self):
        """String representation of the Photo model."""
        return self.title

    def save(self, *args, **kwargs):
        """Override save method to automatically set the url_path."""
        if self.image:
            # Get the relative path from MEDIA_ROOT
            relative_path = os.path.relpath(self.image.path, settings.MEDIA_ROOT)
            # Convert backslashes to forward slashes for URLs
            self.url_path = relative_path.replace('\\', '/')
        super().save(*args, **kwargs)

    class Meta:
        """Meta options for the Photo model."""
        ordering = ['-uploaded_at']  # Most recent photos first
