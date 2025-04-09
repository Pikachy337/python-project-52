from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from .models import User
from .forms import UserRegisterForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
