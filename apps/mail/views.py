"""
Mail Application Views.

This module contains the view functions and classes for the mail application.
It handles all email-related functionality, including:
- Email template rendering
- Email sending
- Email tracking
- Mail-related form processing

The views are responsible for:
- Processing email-related requests
- Managing email templates
- Handling email sending logic
- Tracking email status
"""

# This file contains the views for handling mail-related HTTP requests, such as sending messages and replying to them.
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Message, AdminReply
import logging
from dotenv import load_dotenv
import os
from email.message import EmailMessage
import smtplib
from django.urls import reverse
from django.urls import reverse_lazy
from django.urls import reverse
from django.urls import reverse_lazy

load_dotenv()

logger = logging.getLogger(__name__)

# View to handle the contact form on the home page
# Allows users to send messages to the organization
# Saves the message to the database and sends an email notification
# Handles both GET (show form) and POST (process form) requests
def mail_us(request):
    if request.method == 'POST':
        # Get the message details from the form
        name = request.POST.get('name', 'Anonym')  # Default to 'Anonym' if no name provided
        email = request.POST.get('email', 'Ingen e-post angiven')  # Default message if no email provided
        subject = request.POST.get('subject', 'Inget ämne')
        message_text = request.POST.get('message')
        
        # Create the email content to be sent to the organization
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
            
    # Render the contact form template
    return render(request, 'mail/mail-us.html') 

# View to handle admin replies to user messages
# Allows an admin to reply to a specific message by email and save the reply in the database
def mail_reply(request, message_id):
    # Get the original message by ID, or return 404 if not found
    original_message = get_object_or_404(Message, id=message_id)
    
    if request.method == 'POST':
        # Get reply details from the form
        reply_subject = request.POST.get('subject', f"Re: {original_message.subject or 'Meddelande från webbplatsen'}")
        reply_text = request.POST.get('message')
        
        if not reply_text:
            # If the reply is empty, show an error and re-render the form
            messages.error(request, 'Svaret kan inte vara tomt.')
            return render(request, 'mail/mail-reply.html', {'original_message': original_message})
        
        try:
            # Get email credentials from environment variables
            gmail_address = os.getenv('EMAIL_HOST_USER')
            app_password = os.getenv('EMAIL_HOST_PASSWORD')
            
            # Create the email message to be sent as a reply
            msg = EmailMessage()
            msg['Subject'] = reply_subject
            msg['From'] = gmail_address
            msg['To'] = original_message.email  # Use the email from the original message
            msg.set_content(reply_text)
            
            # Send the email using SMTP with SSL
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(gmail_address, app_password)
                smtp.send_message(msg)
            
            # Save the admin's reply to the database
            AdminReply.objects.create(
                answer_id=original_message.id,
                subject=reply_subject,
                message=reply_text
            )
            
            # Mark the original message as read
            original_message.is_read = True
            original_message.save()
            
            messages.success(request, 'Ditt svar har skickats.')
            return redirect('admin:mail_message_changelist')
            
        except Exception as e:
            # Log the error if sending the reply fails
            logger.error(f"Failed to send reply: {str(e)}")
            messages.error(request, 'Ett fel uppstod när svaret skulle skickas. Vänligen försök igen senare.')
    
    # For GET requests, show the reply form with the original message
    return render(request, 'mail/mail-reply.html', {
        'original_message': original_message,
        'default_subject': f"Re: {original_message.subject or 'Meddelande från webbplatsen'}"
    }) 
        
        