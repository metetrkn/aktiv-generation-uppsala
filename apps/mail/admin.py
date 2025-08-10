"""
Mail Application Admin Configuration.

This module configures the Django admin interface for the mail application models.
It defines how mail-related models are displayed, managed in the Django admin,
including:
- Email template management
- Email sending records
- Email tracking information
- Mail-related settings

The admin interface is designed to provide an intuitive and efficient way to
manage all email-related functionality in the application.
"""

import logging

from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.html import format_html
from .models import AdminReply, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read", "has_reply")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def has_reply(self, obj):
        return AdminReply.objects.filter(answer_id=obj.id).exists()

    has_reply.boolean = True
    has_reply.short_description = "Has Reply"

    def sender_info(self, obj):
        if obj.name and obj.email:
            return f"{obj.name} ({obj.email})"
        elif obj.name:
            return obj.name
        elif obj.email:
            return obj.email
        return "Anonym"

    sender_info.short_description = "Avsändare"

    def status(self, obj):
        if obj.is_read:
            return format_html('<span style="color: blue;">Läst</span>')
        return format_html('<span style="color: red;">Oläst</span>')

    status.short_description = "Status"

    def reply_button(self, obj):
        if obj.email:
            return format_html(
                '<a class="button" href="mailto:{}?subject=Re: {}">Reply</a>',
                obj.email,
                obj.subject or "Meddelande från webbplatsen",
            )
        return "Ingen e-post"

    reply_button.short_description = "Reply"

    def save_model(self, request, obj, form, change):
        if "is_read" in form.changed_data and obj.is_read:
            # Send notification email to the sender if they provided an email
            if obj.email:
                try:
                    send_mail(
                        subject=f"Ditt meddelande har lästs - {settings.ORG_NAME}",
                        message=(
                            f"Hej {obj.name or 'där'}!\n\n"
                            f"Det här är ett automatiskt svar för att bekräfta att vi har mottagit ditt meddelande."
                            f"Vi återkommer så snart som möjligt.\n\n"
                            f"Med vänliga hälsningar,\n"
                            f"{settings.ORG_NAME}"
                        ),
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[obj.email],
                        fail_silently=os.environ.get('FAIL_SILENTLY', False),
                    )
                    logger.info("Email sent successfully")
                except Exception as e:
                    error_msg = f"Kunde inte skicka bekräftelse: {str(e)}"
                    logger.error(error_msg)
                    self.message_user(request, error_msg, level="warning")

        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def has_add_permission(self, request):
        return False

    def response_change(self, request, obj):
        """Override to remove 'Save and continue editing' button"""
        if "_save" in request.POST:
            return self.response_post_save_change(request, obj)
        return super().response_change(request, obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_continue"] = False
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    class Media:
        css = {"all": ("admin/css/message_admin.css",)}


@admin.register(AdminReply)
class AdminReplyAdmin(admin.ModelAdmin):
    list_display = ("get_original_message", "subject", "created_at", "view_original")
    list_filter = ("created_at",)
    search_fields = ("subject", "message", "answer_id")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_original_message(self, obj):
        try:
            original = Message.objects.get(id=obj.answer_id)
            return f"Reply to: {original.subject}"
        except Message.DoesNotExist:
            return f"Reply to message #{obj.answer_id}"

    get_original_message.short_description = "Original Message"

    def view_original(self, obj):
        url = reverse("admin:mail_message_change", args=[obj.answer_id])
        return format_html('<a href="{}">View Original</a>', url)

    view_original.short_description = "View Original Message"

    def response_change(self, request, obj):
        """Override to handle resend functionality"""
        if "_save" in request.POST:
            try:
                # Get the original message
                original_message = Message.objects.get(id=obj.answer_id)

                # Send the email using Django's send_mail
                send_mail(
                    subject=obj.subject,
                    message=obj.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[original_message.email],
                    fail_silently=os.environ.get('FAIL_SILENTLY', False),
                )

                # Update the reply in the database
                obj.save()

                messages.success(request, "Meddelandet har skickats igen.")
                return self.response_post_save_change(request, obj)
            except Exception as e:
                logger.error(f"Failed to resend message: {str(e)}")
                messages.error(
                    request,
                    f"Ett fel uppstod när meddelandet skulle skickas igen: {str(e)}",
                )
                return self.response_post_save_change(request, obj)
        return super().response_change(request, obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_continue"] = False
        extra_context["show_save_and_add_another"] = False
        extra_context["submit_button_text"] = "Resend"
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["submit_button_text"] = "Send"
        return super().add_view(request, form_url, extra_context=extra_context)
