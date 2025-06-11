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
