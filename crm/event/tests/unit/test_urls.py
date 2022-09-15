import pytest

from django.urls import reverse, resolve


@pytest.mark.django_db
def test_event_url():
    path = reverse('event', kwargs={})
    
    assert path == "/api/v1/event/"
    assert resolve(path).view_name == "event"

@pytest.mark.django_db
def test_event_details_url():
    path = reverse('event-details', kwargs={'pk': 1})
    
    assert path == "/api/v1/event/1/"
    assert resolve(path).view_name == "event-details"
