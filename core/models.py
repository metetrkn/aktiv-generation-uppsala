from django.db import models
from django.utils.translation import gettext_lazy as _

class Organization(models.Model):
    name = models.CharField(_('Organization Name'), max_length=200)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=20)
    street = models.CharField(_('Street Address'), max_length=200)
    city = models.CharField(_('City'), max_length=100)
    country = models.CharField(_('Country'), max_length=100)
    postal_code = models.CharField(_('Postal Code'), max_length=20)
    url = models.URLField(_('Website URL'), blank=True)
    description = models.TextField(_('Description'))
    youtube = models.URLField(_('YouTube Channel'), blank=True)
    facebook = models.URLField(_('Facebook Page'), blank=True)
    instagram = models.URLField(_('Instagram Profile'), blank=True)
    logo = models.ImageField(_('Logo'), upload_to='organization/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organization')

    def __str__(self):
        return self.name

class Activity(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    date = models.DateField(_('Date'))
    time = models.TimeField(_('Time'))
    location = models.CharField(_('Location'), max_length=200)
    max_participants = models.PositiveIntegerField(_('Maximum Participants'), null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to='activities/', blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        ordering = ['-date', '-time']

    def __str__(self):
        return self.title 