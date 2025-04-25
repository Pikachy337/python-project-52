from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name=_('Author')
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        null=True,
        blank=True,
        verbose_name=_('Executor')
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabel',
        related_name='tasks',
        blank=True,
        verbose_name=_('Labels')
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-created_at']

    def __str__(self):
        executor_name = self.executor.get_full_name() if self.executor else ""
        return f"{self.name} (Status: {self.status}, Executor: {executor_name})"

    def get_executor_display(self):
        return self.executor.get_full_name() if self.executor else ""


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)

    class Meta:
        unique_together = [['task', 'label']]
