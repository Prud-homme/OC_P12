import pytest

from django.urls import reverse, resolve


@pytest.mark.django_db
def test_contract_url():
    path = reverse('client', kwargs={})
    
    assert path == "/api/v1/client/"
    assert resolve(path).view_name == "client"