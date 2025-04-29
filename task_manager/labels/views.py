from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
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


class LabelDeleteView(SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'general/general_delete_confirm.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Label successfully deleted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Yes, delete')
        return context

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _("Label was deleted successfully"))
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                self.request,
                _("Can't delete, label")
            )
            return redirect(self.success_url)