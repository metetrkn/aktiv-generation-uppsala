from django.db import models
from django.utils import timezone

class Message(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Meddelande'
        verbose_name_plural = 'Meddelanden'

    def __str__(self):
        return f"Meddelande från {self.name or 'Anonym'} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class AdminReply(models.Model):
    answer_id = models.IntegerField()  # Stores the ID of the original message
    subject = models.CharField(max_length=200)
    message = models.TextField()  # The admin's reply message
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Admin Svar'
        verbose_name_plural = 'Admin Svar'

    def __str__(self):
        return f"Svar på meddelande {self.answer_id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
