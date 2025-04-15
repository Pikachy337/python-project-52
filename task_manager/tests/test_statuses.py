from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.forms import Status
from task_manager.tasks.models import Task

User = get_user_model()


class StatusTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass123')
        self.status = Status.objects.create(name='Test Status')
        self.client.login(username='testuser', password='testpass123')

    def test_status_list_view(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status')
        self.assertTemplateUsed(response, 'status/status_list.html')

    def test_status_create_view(self):
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        response = self.client.post(reverse('status_update',
                                            args=[self.status.id]), {
            'name': 'Updated Status'
        })
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view(self):
        response = self.client.post(reverse('status_delete',
                                            args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_protected_status_delete(self):
        Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user
        )

        response = self.client.post(reverse('status_delete',
                                            args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(id=self.status.id).exists())
