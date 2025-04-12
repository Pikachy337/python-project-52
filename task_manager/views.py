from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Task Manager')
        return context


@method_decorator(require_POST, name='dispatch')  # Разрешаем только POST
class LogoutUser(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _("You were logged out"))
        return redirect(reverse_lazy('home'))


class BaseView(LoginRequiredMixin):
    success_message = None

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class OwnerOnlyMixin(UserPassesTestMixin):
    permission_denied_message = _("You don't have permission to do this")

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return super().handle_no_permission()


class ProtectedDeleteMixin:
    protected_message = None
    protected_url = None

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except models.ProtectedError:
            messages.error(self.request, self.protected_message)
            return redirect(self.protected_url)
