from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Message
import logging

logger = logging.getLogger(__name__)

# To handle HTTP requests and responses in home page
def mail_us(request):
    if request.method == 'POST':
        # Get the message details from the form
        name = request.POST.get('name', 'Anonym')  # Default to 'Anonym' if no name provided
        email = request.POST.get('email', 'Ingen e-post angiven')  # Default message if no email provided
        subject = request.POST.get('subject', 'Inget ämne')
        message_text = request.POST.get('message')
        
        # Create the email content
        email_subject = f'Meddelande från webbplatsen: {subject}'
        email_message = (
            f"Ett nytt meddelande har skickats från webbplatsen\n\n"
            f"Från: {name}\n"
            f"E-post: {email}\n"
            f"Ämne: {subject}\n\n"

            f"Meddelande:\n"
            f"{message_text}"
        )
        
        try:
            # Save message to database
            Message.objects.create(
                name=name if name != 'Anonym' else None,
                email=email if email != 'Ingen e-post angiven' else None,
                subject=subject if subject != 'Inget ämne' else None,
                message=message_text
            )
            
            # Log the attempt to send email
            logger.info(f"Attempting to send email to {settings.ORG_EMAIL}")
            logger.info(f"Using EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            
            # Send the message to the organization's email
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.EMAIL_HOST_USER,  # This is your organization's email
                recipient_list=[settings.ORG_EMAIL],  # This is where you'll receive the messages
                fail_silently=False,
            )
            messages.success(request, 'Tack för ditt meddelande! Vi återkommer så snart som möjligt.')
            logger.info("Email sent successfully")
        except Exception as e:
            # Log the actual error
            logger.error(f"Failed to send email: {str(e)}")
            messages.error(request, 'Ett fel uppstod när meddelandet skulle skickas. Vänligen försök igen senare.')
            
    return render(request, 'mail/mail-us.html') 