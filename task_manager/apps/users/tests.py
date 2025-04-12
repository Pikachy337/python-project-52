from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            first_name='Admin',
            last_name='User'
        )

    def test_user_list_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertTemplateUsed(response, 'user/user_list.html')

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('user_update', args=[self.user.id]), {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'updateduser',
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('user_delete', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_cannot_delete_other_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('user_delete', args=[self.admin.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(id=self.admin.id).exists())
