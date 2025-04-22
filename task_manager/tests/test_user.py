from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            first_name='Test',
            last_name='User'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass',
            first_name='Other',
            last_name='User'
        )

    def test_user_create_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_user_list_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.get_full_name())

    def test_user_delete_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('user_delete',
                                            args=[self.admin.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.admin.id).exists())

        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_delete',
                                            args=[self.other_user.id]))
        self.assertEqual(response.status_code, 302)

    def test_cannot_delete_other_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_delete',
                                            args=[self.admin.id]))
        self.assertEqual(response.status_code, 302)
