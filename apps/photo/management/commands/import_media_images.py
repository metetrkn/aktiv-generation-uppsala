"""
Management command to import images from the media/core/images directory into the database.

This script scans the specified media directory for image files and creates Photo objects
in the database for each image that does not already exist, based on its URL path.
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.photo.models import Photo

class Command(BaseCommand):
    """
    Django management command to import images from media/core/images into the Photo model.
    """
    help = 'Import images from media/core/images directory into the database'

    def handle(self, *args, **options):
        """
        Main entry point for the command. Scans the media/core/images directory for image files
        and imports them into the Photo model if they do not already exist.
        """
        media_images_dir = os.path.join(settings.MEDIA_ROOT, 'core', 'images')
        if not os.path.exists(media_images_dir):
            self.stdout.write(self.style.ERROR(f'Directory not found: {media_images_dir}'))
            return

        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        imported_count = 0
        skipped_count = 0

        for filename in os.listdir(media_images_dir):
            if filename.lower().endswith(image_extensions):
                url_path = f'core/images/{filename}'
                # Only import if a Photo with this url_path does not already exist
                if not Photo.objects.filter(url_path=url_path).exists():
                    title = os.path.splitext(filename)[0]
                    Photo.objects.create(
                        title=title,
                        image=url_path,  # This works if your ImageField is set up with MEDIA_ROOT
                        url_path=url_path,
                        description=f'Imported from media images: {filename}'
                    )
                    imported_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Imported: {filename}'))
                else:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f'Skipped (already exists): {filename}'))

        self.stdout.write(self.style.SUCCESS(
            f'Import completed. Imported: {imported_count}, Skipped: {skipped_count}'
        )) 