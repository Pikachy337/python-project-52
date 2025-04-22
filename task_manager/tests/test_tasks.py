from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.forms import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TaskTestCase(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name='Test Status')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass'
        )
        self.task = Task.objects.create(
            name='Test Task',
            status=self.status,
            author=self.user
        )

    def test_task_list_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

    def test_TaskCreate(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)

    def test_task_delete_by_author(self):
        self.client.login(username='author', password='testpass123')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

    def test_task_delete_by_non_author(self):
        self.client.login(username='otheruser', password='testpass')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
