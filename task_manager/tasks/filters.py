import django_filters
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.labels.forms import Label
from task_manager.statuses.forms import Status

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

    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Author'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label=_('Only my tasks'),
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'author', 'self_tasks']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def filter_self_tasks(self, queryset, name, value):
        if value and self.user:
            return queryset.filter(author=self.user)
        return queryset
