import pytest

from django.urls import reverse
from crm.event.models import Event
from datetime import datetime
import json

@pytest.mark.django_db
class TestEvent():

    post_data = {
        "client_id": 1,
        "support_contact_id": 1,
        "event_status": "ongoing",
        "attendees": 1000,
        "event_date": datetime(2022, 9, 15).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
        "notes": "Event Test",
    }

    event_path = reverse('event', kwargs={})

    def test_event_post_method_sales_user(self, api_client_with_credentials_sales):
        response = api_client_with_credentials_sales.post(self.event_path, self.post_data)
        content = response.content.decode()
        data_to_compare = {key: value for key, value in json.loads(content).items() if key != "id"}

        assert response.status_code == 201
        assert self.post_data == data_to_compare

    def test_event_post_method_support_user(self, api_client_with_credentials_support):
        response = api_client_with_credentials_support.post(self.event_path, self.post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        
        assert response.status_code == 403
        assert detail_message == "Vous n'avez pas la permission d'effectuer cette action."

    def test_event_post_method_management_user(self, api_client_with_credentials_management):
        response = api_client_with_credentials_management.post(self.event_path, self.post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]

        assert response.status_code == 403
        assert detail_message == "Vous n'avez pas la permission d'effectuer cette action."
