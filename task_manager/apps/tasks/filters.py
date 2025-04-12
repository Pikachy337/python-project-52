import django_filters
from django.utils.translation import gettext_lazy as _
from .models import Task
from django import forms


class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(
        field_name='status__name',
        lookup_expr='icontains',
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = django_filters.CharFilter(
        field_name='executor__username',
        lookup_expr='icontains',
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    labels = django_filters.CharFilter(
        field_name='labels__name',
        lookup_expr='icontains',
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

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
