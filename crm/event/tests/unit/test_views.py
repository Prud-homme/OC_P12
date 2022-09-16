import pytest

from django.urls import reverse
from crm.event.models import Event
from datetime import datetime
import json

@pytest.mark.django_db
class TestEvent():

    event_path = reverse('event', kwargs={})
    event_details_path = reverse('event-details', kwargs={"pk": 1})

    def test_event_post_method(self, api_client, crm):
        client_a = crm["client_a"]
        sales_user_a = crm["sales_user_a"]
        support_user_a = crm["support_user_a"]
        management_user = crm["management_user"]

        post_data = {
            "client_id": client_a.id,
            "support_contact_id": support_user_a.id,
            "event_status": "ongoing",
            "attendees": 1000,
            "event_date": datetime(2022, 9, 15).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
            "notes": "Event Test",
        }

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.post(self.event_path, post_data)
        content = response.content.decode()
        data_to_compare = {key: value for key, value in json.loads(content).items() if key != "id"}
        assert response.status_code == 201
        assert post_data == data_to_compare

        api_client.force_authenticate(user=support_user_a)
        response = api_client.post(self.event_path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert detail_message == "Vous n'avez pas la permission d'effectuer cette action."

        api_client.force_authenticate(user=management_user)
        response = api_client.post(self.event_path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert detail_message == "Vous n'avez pas la permission d'effectuer cette action."

        api_client.force_authenticate(user=None)

