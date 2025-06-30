import os

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.photo.models import Photo


class Command(BaseCommand):
    help = "Import images from core/static/core/images directory into the database"

    def handle(self, *args, **options):
        # Path to the static images directory
        static_images_dir = os.path.join(
            settings.BASE_DIR, "apps", "core", "static", "core", "images"
        )

        # Check if directory exists
        if not os.path.exists(static_images_dir):
            self.stdout.write(
                self.style.ERROR(f"Directory not found: {static_images_dir}")
            )
            return

        # Get all image files
        image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
        imported_count = 0
        skipped_count = 0

        for filename in os.listdir(static_images_dir):
            if filename.lower().endswith(image_extensions):
                # Create URL path
                url_path = f"core/images/{filename}"

                # Check if photo with this URL already exists
                if not Photo.objects.filter(url_path=url_path).exists():
                    # Create new photo entry
                    title = os.path.splitext(filename)[
                        0
                    ]  # Use filename without extension as title
                    Photo.objects.create(
                        title=title,
                        url_path=url_path,
                        description=f"Imported from static images: {filename}",
                    )
                    imported_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Imported: {filename}"))
                else:
                    skipped_count += 1
                    self.stdout.write(
                        self.style.WARNING(f"Skipped (already exists): {filename}")
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed. Imported: {imported_count}, Skipped: {skipped_count}"
            )
        )
