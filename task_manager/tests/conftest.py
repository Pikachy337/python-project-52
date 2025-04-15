import pytest
from django.core.management import call_command
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('migrate', '--noinput')


@pytest.fixture(autouse=True)
def load_users(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'users.json')


@pytest.fixture(autouse=True)
def load_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'users.json')
