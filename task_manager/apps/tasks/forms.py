from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.apps.statuses.models import Status
from task_manager.apps.labels.models import Label
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        widget=forms.SelectMultiple,
        label=_('Labels')
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'executor': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
