import pytest

from django.urls import reverse, resolve


@pytest.mark.django_db
def test_event_urls():
    path = reverse('event', kwargs={})
    
    assert path == "/api/v1/event/"
    assert resolve(path).view_name == "event"
