from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(max_length=150, verbose_name=_('First name'))
    last_name = models.CharField(max_length=150, verbose_name=_('Last name'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))

    class Meta:
        db_table = 'users_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)
