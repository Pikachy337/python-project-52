from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


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
        context['button'] = _('Create')
        return context


class LabelUpdateView(SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'general/general_form.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Label successfully updated')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Change')
        return context


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'general/general_delete_confirm.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Label successfully deleted')
    error_message = _('Cannot delete label')

    def form_valid(self, form):
        if self.get_object().tasks.exists():
            messages.error(self.request, self.error_message)
            return redirect(self.success_url)

        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Delete label'),
            'button': _('Yes, delete')
        })
        return context