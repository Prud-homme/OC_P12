import pytest
from django.urls import resolve, reverse


@pytest.mark.django_db
def test__token_urls():
    path = reverse("token_obtain_pair", kwargs={})

    assert path == "/api/v1/token/"
    assert resolve(path).view_name == "token_obtain_pair"

    path = reverse("token_refresh", kwargs={})

    assert path == "/api/v1/token/refresh/"
    assert resolve(path).view_name == "token_refresh"
