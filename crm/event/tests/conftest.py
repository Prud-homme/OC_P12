import uuid

import pytest

from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


@pytest.fixture
def api_client():
   return APIClient()

@pytest.fixture
def test_password():
   return '?2.PabY8MB'

@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user

@pytest.fixture
def api_client_with_credentials_sales(
        db, create_user, api_client
    ):
    user = create_user()

    group = Group.objects.get(name='sales')
    user.groups.add(group)

    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def api_client_with_credentials_support(
        db, create_user, api_client
    ):
    user = create_user()

    group = Group.objects.get(name='support')
    user.groups.add(group)

    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)

@pytest.fixture
def api_client_with_credentials_management(
       db, create_user, api_client
    ):
    user = create_user()

    user.is_staff = True
    group = Group.objects.get(name='management')
    user.groups.add(group)

    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
