from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.db import models
from .models import Status
from .forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'status/status_list.html'
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Statuses')
        context['button'] = _('Create status')
        return context


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'general/general_form.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create status')
        context['button'] = _('Create')
        return context


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'general/general_form.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully updated')

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Update status')
        context['button'] = _('Update')
        return context


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'general/general_delete_confirm.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    protected_message = _('Cannot delete status because it is in use')
    protected_url = reverse_lazy('statuses')

    def form_valid(self, form):
        try:
            messages.success(self.request, self.success_message)
            return super().form_valid(form)
        except models.ProtectedError:
            messages.error(self.request, self.protected_message)
            return redirect(self.protected_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete status')
        context['button'] = _('Yes, delete')
        return context
