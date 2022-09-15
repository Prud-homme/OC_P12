import pytest

from django.urls import reverse, resolve


@pytest.mark.django_db
def test_contract_url():
    path = reverse('contract', kwargs={})
    
    assert path == "/api/v1/contract/"
    assert resolve(path).view_name == "contract"