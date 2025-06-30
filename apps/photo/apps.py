from django.apps import AppConfig


class PhotoConfig(AppConfig):
    """
    Configuration class for the Photo application.

    This class defines the configuration settings for the photo app,
    including the default primary key field type and the app name.
    """

    default_auto_field = (
        "django.db.models.BigAutoField"  # Use 64-bit integer as primary key
    )
    name = "apps.photo"  # The name of the application
