from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.forms import Label

User = get_user_model()


class LabelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.label = Label.objects.create(name='Test Label')

    def test_label_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Label')
        self.assertTemplateUsed(response, 'label/label_list.html')

    def test_label_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('labels:create'), {
            'name': 'New Label'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('labels:delete',
                                            args=[self.label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())
