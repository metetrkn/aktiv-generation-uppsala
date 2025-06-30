"""
Mail Application Models.

This module defines the database models for the mail application, including:
- Email templates
- Email sending records
- Email tracking information
- Mail-related settings

These models are used to store and manage all email-related data in the application,
including templates, sending history, and tracking information.
"""

# This file defines the database models for the mail app, including user messages and admin replies.
from django.db import models
from django.utils import timezone


class Message(models.Model):
    """
    Represents a message sent by a user via the contact form.

    Attributes:
        name (str): Sender's name, optional.
        email (str): Sender's email address, optional.
        subject (str): Message subject, optional.
        message (str): Content of the message.
        created_at (datetime): Timestamp of creation.
        is_read (bool): Whether the message has been read by admin.
    """

    # Name of the sender (can be blank or null)
    name = models.CharField(max_length=100, blank=True, null=True)
    # Email address of the sender (can be blank or null)
    email = models.EmailField(blank=True, null=True)
    # Subject of the message (can be blank or null)
    subject = models.CharField(max_length=200, blank=True, null=True)
    # The actual message content
    message = models.TextField()
    # Timestamp when the message was created
    created_at = models.DateTimeField(default=timezone.now)
    # Boolean indicating if the message has been read by an admin
    is_read = models.BooleanField(default=False)

    class Meta:
        """
        Model metadata.

        Orders messages by newest first.
        Sets verbose names for admin display.
        """

        # Order messages by creation date, newest first
        ordering = ["-created_at"]
        # Human-readable singular and plural names for the admin interface
        verbose_name = "Meddelande"
        verbose_name_plural = "Meddelanden"

    def __str__(self):
        # String representation of the message, showing sender and date
        return f"Meddelande från {self.name or 'Anonym'} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class AdminReply(models.Model):
    """
    Stores replies sent by admins to user messages.

    Attributes:
        answer_id (int): ID of the original message being replied to.
        subject (str): Subject of the admin's reply.
        message (str): Content of the reply message.
        created_at (datetime): Timestamp when the reply was created.
    """

    # ID of the original message being replied to
    answer_id = models.IntegerField()  # Stores the ID of the original message
    # Subject of the admin's reply
    subject = models.CharField(max_length=200)
    # The reply message content
    message = models.TextField()  # The admin's reply message
    # Timestamp when the reply was created
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """
        Model metadata.

        Orders replies by newest first.
        Sets verbose names for admin interface.
        """

        # Order replies by creation date, newest first
        ordering = ["-created_at"]
        # Human-readable singular and plural names for the admin interface
        verbose_name = "Admin Svar"
        verbose_name_plural = "Admin Svar"

    def __str__(self):
        """
        Return a string showing the original message ID and reply date.
        """

        return f"Svar på meddelande {self.answer_id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
