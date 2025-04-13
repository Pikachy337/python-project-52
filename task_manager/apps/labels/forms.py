from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Label name')
            }),
        }
        labels = {
            'name': _('Name'),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Label.objects.filter(name=name).exists():
            if self.instance.pk is None or self.instance.name != name:
                raise forms.ValidationError(_('Label with this name'
                                              ' already exists'))
        return name
