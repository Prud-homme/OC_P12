import uuid

import pytest

from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from datetime import datetime
from crm.event.models import Event
from crm.client.models import Client
from crm.contract.models import Contract


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
def crm(db, create_user):
    sales_user_a = create_user()
    sales_user_b = create_user()
    group = Group.objects.get(name='sales')
    sales_user_a.groups.add(group)
    sales_user_b.groups.add(group)

    support_user_a = create_user()
    support_user_b = create_user()
    group = Group.objects.get(name='support')
    support_user_a.groups.add(group)
    support_user_b.groups.add(group)

    management_user = create_user()
    management_user.is_staff = True
    group = Group.objects.get(name='management')
    management_user.groups.add(group)

    client_a = Client.objects.create(
        firstname="John",
        lastname="Doe",
        email="johndoe@example.com", 
        phone="0000000000",
        mobile="0000000000",
        company_name="Example",
        sales_contact_id=sales_user_a,
    )

    event_a = Event.objects.create(
        client_id=client_a,
        support_contact_id=support_user_a,
        event_status="ongoing",
        attendees=1000,
        event_date=datetime(2022, 9, 18).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
        notes="Event A",
    )

    contract_a = Contract.objects.create(
        sales_contact_id = sales_user_a,
        client_id = client_a,
        status = True,
        amount = 10000.99,
        payment_due = datetime(2022, 8, 10).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
    )

    config = {
        "sales_user_a": sales_user_a,
        "sales_user_b": sales_user_b,
        "support_user_a": support_user_a,
        "support_user_b": support_user_b,
        "management_user": management_user,
        "client_a": client_a,
        "event_a": event_a,
        "contract_a": contract_a,

    }
    return config

@pytest.fixture
def api_client_with_credentials(
        db, create_user, api_client,
    ):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
