from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserForm
from .models import User


class UserListView(ListView):
    model = User
    template_name = 'user/list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Users')
        return context


class CustomLoginView(LoginView):
    template_name = 'general/general_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Login')
        context['button'] = _('Enter')
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'general/general_form.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Registration')
        context['button'] = _('Register')
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'general/general_form.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully updated')
    permission_denied_message = _("You don't have"
                                  " permission to edit another user")

    def test_func(self):
        return self.get_object() == self.request.user

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit user')
        context['button'] = _('Update')
        return context


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'general/general_delete_confirm.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')
    permission_denied_message = _("You don't have"
                                  " permission to delete another user")
    protected_message = _('Cannot delete user because it is in use')
    protected_url = reverse_lazy('users')

    def test_func(self):
        return self.get_object() == self.request.user

    def form_valid(self, form):
        try:
            messages.success(self.request, self.success_message)
            return super().form_valid(form)
        except models.ProtectedError:
            messages.error(self.request, self.protected_message)
            return redirect(self.protected_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete user')
        context['button'] = _('Yes, delete')
        return context
