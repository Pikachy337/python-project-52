# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.shortcuts import redirect
# from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _
#
#
# class AuthenticationMixin(LoginRequiredMixin):
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             messages.error(
#                 request,
#                 messages.error(self.request, _("You are not authenticated."))
#             )
#             return redirect(reverse_lazy("login"))
#         return super(
#             LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
#
#
# class AuthorizationMixin(UserPassesTestMixin):
#
#     def test_func(self):
#         return self.kwargs.get('pk') == self.request.user.pk
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.test_func():
#             messages.error(
#                 request,
#                 messages.error(
#                     self.request, _(
#                         "You haven't permission for changing another user."))
#             )
#             return redirect(reverse_lazy("users"))
#         return super(
#             UserPassesTestMixin, self).dispatch(request, *args, **kwargs)
#
#
# class AuthorizationTaskMixin(UserPassesTestMixin):
#
#     def test_func(self):
#         return self.get_object().author.pk == self.request.user.pk
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.test_func():
#             messages.error(
#                 request,
#                 messages.error(
#                     self.request, _(
#                         "The task can only be deleted by its author."))
#             )
#             return redirect(reverse_lazy("tasks"))
#         return super().dispatch(request, *args, **kwargs)
