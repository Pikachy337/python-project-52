from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from .models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_executor'
        }),
        required=False,
        label=_('Executor')
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'size': '4'
        }),
        required=False,
        label=_('Labels')
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
