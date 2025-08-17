"""
Core Application Models.

This module defines the database models for the core application,
which manages activities and related data.

Models included:
- Activity: Represents events or activities organized by the organization.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings


class Activity(models.Model):
    """
    Model representing an activity or event, with details such as title,
    schedule, location, and participant limits.
    """

    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)
    date = models.DateField(_("Date"), blank=True, null=True)
    time = models.TimeField(_("Time"), blank=True, null=True)
    location = models.CharField(_("Location"), max_length=200, blank=True, null=True)
    max_participants = models.PositiveIntegerField(
        _("Maximum Participants"), null=True, blank=True
    )
    future_event = models.BooleanField(_("Future Event"), default=False, help_text=_('Check if this is a future event.'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Metadata for the Activity model.

        - verbose_name: Singular name for the model in admin interfaces.
        - verbose_name_plural: Plural name for the model in admin interfaces.
        - ordering: Default ordering of query results by date descending, then time descending.
        """

        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")
        ordering = ["-date", "-time"]

    def __str__(self):
        """
        Return the activity title as the string representation.
        """

        return self.title


class ActivityImage(models.Model):
    """
    Model to store multiple images for a single Activity.
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(_("Image"), upload_to="activities/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.activity.title}"

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)
