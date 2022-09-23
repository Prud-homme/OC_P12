import uuid
from datetime import datetime

import pytest
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from crm.client.models import Client
from crm.client.serializers import ClientSerializer
from crm.contract.models import Contract
from crm.contract.serializers import ContractSerializer
from crm.event.models import Event
from crm.event.serializers import EventSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return "?2.PabY8MB"


@pytest.fixture  # @pytest.mark.django_db
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture  # @pytest.mark.django_db
def create_superuser(db, django_user_model, test_password):
    def make_superuser(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        kwargs["email"] = kwargs["username"] + "@example.com"
        return django_user_model.objects.create_superuser(**kwargs)

    return make_superuser


@pytest.fixture
@pytest.mark.django_db
def crm(db, create_user, create_superuser):
    superuser = create_superuser()

    sales_user_a = create_user()
    sales_user_b = create_user()
    group = Group.objects.get(name="sales")
    sales_user_a.groups.add(group)
    sales_user_b.groups.add(group)

    support_user_a = create_user()
    support_user_b = create_user()
    group = Group.objects.get(name="support")
    support_user_a.groups.add(group)
    support_user_b.groups.add(group)

    management_user = create_user()
    management_user.is_staff = True
    group = Group.objects.get(name="management")
    management_user.groups.add(group)

    client_a = Client.objects.create(
        firstname="John",
        lastname="Doe",
        email="johndoe@example.com",
        phone="0000000000",
        mobile="0000000000",
        company_name="Example",
        sales_contact=sales_user_a,
    )
    serializer = ClientSerializer(client_a)
    serial_client_a = serializer.data

    client_b = Client.objects.create(
        firstname="Jane",
        lastname="Doe",
        email="janedoe@example.com",
        phone="0000000000",
        mobile="0000000000",
        company_name="Example",
        sales_contact=sales_user_a,
    )

    event_a = Event.objects.create(
        client=client_a,
        support_contact=support_user_a,
        event_status="ongoing",
        attendees=1000,
        event_date=datetime(2022, 9, 18).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
        notes="Event A",
    )
    serializer = EventSerializer(event_a)
    serial_event_a = serializer.data

    contract_a = Contract.objects.create(
        sales_contact=sales_user_a,
        client=client_a,
        status=True,
        amount=10000.99,
        payment_due=datetime(2022, 8, 10).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
    )
    serializer = ContractSerializer(contract_a)
    serial_contract_a = serializer.data

    config = {
        "superuser": superuser,
        "sales_user_a": sales_user_a,
        "sales_user_b": sales_user_b,
        "support_user_a": support_user_a,
        "support_user_b": support_user_b,
        "management_user": management_user,
        "client_a": client_a,
        "serial_client_a": serial_client_a,
        "client_b": client_b,
        "event_a": event_a,
        "serial_event_a": serial_event_a,
        "contract_a": contract_a,
        "serial_contract_a": serial_contract_a,
    }
    return config
