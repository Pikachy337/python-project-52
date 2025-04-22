from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Status, Task

User = get_user_model()


class FilterTestCase(TestCase):
    def setUp(self):
        self.status1 = Status.objects.create(name='online-test')
        self.status2 = Status.objects.create(name='offline-test')
        self.author1 = User.objects.create_user(username='author1')
        self.author2 = User.objects.create_user(username='author2')
        self.executor1 = User.objects.create_user(username='executor1')
        self.executor2 = User.objects.create_user(username='executor2')

        self.task1 = Task.objects.create(
            name='Task 1',
            status=self.status1,
            author=self.author1,
            executor=self.executor1
        )
        self.task2 = Task.objects.create(
            name='Task 2',
            status=self.status2,
            author=self.author2,
            executor=self.executor2
        )

    def login(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_status(self):
        filter = TaskFilter({'status': self.status1.id})
        self.assertEqual(filter.qs.first().status.name, 'online-test')

    def test_executor(self):
        filter = TaskFilter({'executor': self.executor1.id})
        self.assertEqual(filter.qs.count(), 1)
        self.assertEqual(filter.qs.first().executor, self.executor1)

    def test_author(self):
        filter = TaskFilter({'author': self.author1.id})
        self.assertEqual(filter.qs.count(), 2)
        # self.assertEqual(filter.qs.first().author, self.author1)
