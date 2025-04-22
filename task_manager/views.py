from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Task Manager')
        return context


class LoginUser(SuccessMessageMixin, LoginView):
    template_name = 'general/general_form.html'
    success_message = _('You were successfully logged in!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Login'),
            'button': _('Enter')
        })
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUser(DjangoLogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You were logged out"))
        return super().dispatch(request, *args, **kwargs)
