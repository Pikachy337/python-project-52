from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Status

User = get_user_model()


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.status = Status.objects.create(name='Test Status')
        self.client.login(username='testuser', password='testpass123')

    def test_status_list_view(self):
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status')

    def test_status_create_view(self):
        response = self.client.post(reverse('statuses:create'), {
            'name': 'New Status'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        response = self.client.post(
            reverse('statuses:update', args=[self.status.id]),
            {'name': 'Updated Status'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view(self):
        response = self.client.post(
            reverse('statuses:delete', args=[self.status.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())


class StatusAccessTest(TestCase):
    def test_unauthenticated_access(self):
        urls = [
            reverse('statuses:list'),
            reverse('statuses:create'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/login/?next={url}')
