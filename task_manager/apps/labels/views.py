from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from .models import Label
from .forms import LabelForm


class LabelListView(ListView):
    model = Label
    template_name = 'label/label_list.html'
    context_object_name = 'labels'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Labels')
        context['button'] = _('Create label')
        return context


class LabelCreateView(SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'general/general_form.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Label successfully created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create label')
        return context


class LabelUpdateView(SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'general/general_form.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Label successfully updated')


class LabelDeleteView(SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'general/general_delete_confirm.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Label successfully deleted')
