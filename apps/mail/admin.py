from django.contrib import admin
from django.utils.html import format_html
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Message
import logging

logger = logging.getLogger(__name__)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_info', 'subject', 'created_at', 'status', 'reply_button')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    fieldsets = (
        ('Meddelande Information', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )

    def sender_info(self, obj):
        if obj.name and obj.email:
            return f"{obj.name} ({obj.email})"
        elif obj.name:
            return obj.name
        elif obj.email:
            return obj.email
        return "Anonym"
    sender_info.short_description = 'Avsändare'

    def status(self, obj):
        if obj.is_read:
            return format_html('<span style="color: blue;">Läst</span>')
        return format_html('<span style="color: red;">Oläst</span>')
    status.short_description = 'Status'

    def reply_button(self, obj):
        if obj.email:
            return format_html(
                '<a class="button" href="mailto:{}?subject=Re: {}">Reply</a>',
                obj.email,
                obj.subject or 'Meddelande från webbplatsen'
            )
        return "Ingen e-post"
    reply_button.short_description = 'Reply'

    def save_model(self, request, obj, form, change):
        if 'is_read' in form.changed_data and obj.is_read:
            # Send notification email to the sender if they provided an email
            if obj.email:
                try:
                    email = EmailMessage(
                        subject=f'Ditt meddelande har lästs - {settings.ORG_NAME}',
                        body=(
                            f"Hej {obj.name or 'där'}!\n\n"
                            
                            f"Det här är ett automatiskt svar för att bekräfta att vi har mottagit ditt meddelande. Vi återkommer så snart som möjligt.\n\n"

                            f"Med vänliga hälsningar,\n"
                            f"{settings.ORG_NAME}"
                        ),
                        from_email=settings.EMAIL_HOST_USER,
                        to=[obj.email],
                    )
                    email.send(fail_silently=True)
                    logger.info("Email sent successfully")
                except Exception as e:
                    error_msg = f"Kunde inte skicka bekräftelse: {str(e)}"
                    logger.error(error_msg)
                    self.message_user(request, error_msg, level='warning')
        
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def response_change(self, request, obj):
        """Override to remove 'Save and continue editing' button"""
        if "_save" in request.POST:
            return self.response_post_save_change(request, obj)
        return super().response_change(request, obj)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    class Media:
        css = {
            'all': ('admin/css/message_admin.css',)
        }
