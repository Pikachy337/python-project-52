from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from .models import Label

User = get_user_model()


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.label = Label.objects.create(name='Test Label')
        self.client.login(username='testuser', password='testpass123')

    def test_label_list_view(self):
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Label')

    def test_label_create_view(self):
        response = self.client.post(reverse('labels:create'), {
            'name': 'New Label'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_update_view(self):
        response = self.client.post(
            reverse('labels:update', args=[self.label.id]),
            {'name': 'Updated Label'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_delete_view(self):
        response = self.client.post(
            reverse('labels:delete', args=[self.label.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_label_delete_with_task(self):
        task = Task.objects.create(
            name='Test Task',
            description='Test',
            status=Status.objects.create(name='Test'),
            author=self.user
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse('labels:delete', args=[self.label.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())


class LabelAccessTest(TestCase):
    def test_unauthenticated_access(self):
        urls = [
            reverse('labels:list'),
            reverse('labels:create'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'/login/?next={url}')
