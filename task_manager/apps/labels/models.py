from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.apps.tasks.models import Task


class Label(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Name')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    tasks = models.ManyToManyField(
        Task,
        related_name='labels',
        blank=True,
        verbose_name=_('Tasks')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
