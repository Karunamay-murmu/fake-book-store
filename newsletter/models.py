
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email


class Subscriber(models.Model):
    email = models.EmailField(
        _('email address'), max_length=255, blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
        ordering = ('created_at', 'updated_at')

    def __str__(self):
        return self.email
