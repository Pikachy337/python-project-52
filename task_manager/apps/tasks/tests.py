from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.apps.statuses.models import Status
from task_manager.apps.labels.models import Label
from .models import Task

User = get_user_model()


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.status1 = Status.objects.create(name='Status 1')
        self.status2 = Status.objects.create(name='Status 2')
        self.label1 = Label.objects.create(name='Label 1')
        self.label2 = Label.objects.create(name='Label 2')

        self.task1 = Task.objects.create(
            name='Task 1',
            description='Desc 1',
            status=self.status1,
            author=self.user,
            executor=self.other_user
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Task 2',
            description='Desc 2',
            status=self.status2,
            author=self.other_user,
            executor=self.user
        )
        self.task2.labels.add(self.label2)

    def test_filter_by_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('tasks:list') + f'?status={self.status1.id}'
        )
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_executor(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('tasks:list') + f'?executor={self.user.id}'
        )
        self.assertContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 1')

    def test_filter_by_label(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('tasks:list') + f'?labels={self.label1.id}'
        )
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_self_tasks(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('tasks:list') + '?self_tasks=on'
        )
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
