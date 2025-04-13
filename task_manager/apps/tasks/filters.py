import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from task_manager.apps.statuses.models import Status
from task_manager.apps.labels.models import Label
from .models import Task

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    labels = django_filters.ModelChoiceFilter(
        field_name='tasklabel__label',
        queryset=Label.objects.all(),
        label=_('Label'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label=_('Only my tasks'),
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def filter_self_tasks(self, queryset, name, value):
        if value and self.user:  # Проверяем наличие пользователя
            return queryset.filter(author=self.user)
        return queryset