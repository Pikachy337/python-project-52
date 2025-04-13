from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')

    def __str__(self):
        return self.name
