from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Name')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
        ordering = ['name']

    def __str__(self):
        return self.name
