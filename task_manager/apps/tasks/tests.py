from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.apps.statuses.models import Status
from .models import Task

User = get_user_model()


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user
        )

    def test_task_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        self.assertTemplateUsed(response, 'task/task_list.html')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_delete_by_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_delete_by_non_author(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
