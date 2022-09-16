import pytest
from django.urls import resolve, reverse


@pytest.mark.django_db
def test_contract_url():
    path = reverse("client", kwargs={})

    assert path == "/api/v1/client/"
    assert resolve(path).view_name == "client"


@pytest.mark.django_db
def test_contract_details_url():
    path = reverse("client-details", kwargs={"pk": 1})

    assert path == "/api/v1/client/1/"
    assert resolve(path).view_name == "client-details"
