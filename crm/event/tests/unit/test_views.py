import copy
import json
from datetime import datetime

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestEvent:

    event_path = reverse("event", kwargs={})

    def test_create_event_post_method(self, api_client, crm):
        client_a = crm["client_a"]
        sales_user_a = crm["sales_user_a"]
        support_user_a = crm["support_user_a"]
        management_user = crm["management_user"]
        contract_a = crm["contract_a"]

        post_data = {
            "client": client_a.id,
            "contract": contract_a.id,
            "support_contact": support_user_a.id,
            "event_status": "ongoing",
            "attendees": 1000,
            "event_date": datetime(2022, 9, 15).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
            "notes": "Event Test",
        }

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.post(self.event_path, post_data)
        content = response.content.decode()
        data_to_compare = {
            key: value for key, value in json.loads(content).items() if key != "id"
        }
        assert response.status_code == 201
        assert post_data == data_to_compare

        api_client.force_authenticate(user=support_user_a)
        response = api_client.post(self.event_path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=management_user)
        response = api_client.post(self.event_path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=None)

    def test_read_event_get_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        support_user_a = crm["support_user_a"]
        support_user_b = crm["support_user_b"]
        management_user = crm["management_user"]
        event_a = crm["event_a"]
        serial_event_a = crm["serial_event_a"]

        path = reverse("event-details", kwargs={"pk": event_a.id})

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.get(path)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=support_user_a)
        response = api_client.get(path)
        content = response.content.decode()
        data = json.loads(content)
        assert response.status_code == 200
        assert data == serial_event_a

        api_client.force_authenticate(user=support_user_b)
        response = api_client.get(path)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 404
        assert detail_message == "Pas trouvé."

        api_client.force_authenticate(user=management_user)
        response = api_client.get(path)
        content = response.content.decode()
        data = json.loads(content)
        assert response.status_code == 200
        assert data == serial_event_a

        response = api_client.get(self.event_path)
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 2

        response = api_client.get(self.event_path + "?date=2022-09-18")
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 2

        response = api_client.get(self.event_path + "?date=2021-09-18")
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 0

        response = api_client.get(self.event_path + "?email=janedoe@example.com")
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 1

        response = api_client.get(self.event_path + "?email=jagrnedoe@example.com")
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 0

        response = api_client.get(self.event_path + "?lastname=doe")
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 2

        response = api_client.get(self.event_path + "?lastname=irvng")
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 0

        response = api_client.get(
            self.event_path + "?email=janedoe@example.com&lastname=doe"
        )
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 1

        response = api_client.get(self.event_path + "?title=janedoe@example.com")
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 400
        assert detail_message == "Le(s) filtre(s) n'existe(nt) pas"

        api_client.force_authenticate(user=None)

    def test_update_event_put_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        support_user_a = crm["support_user_a"]
        support_user_b = crm["support_user_b"]
        management_user = crm["management_user"]
        client_a = crm["client_a"]
        client_b = crm["client_b"]
        event_a = crm["event_a"]
        contract_a = crm["contract_a"]

        path = reverse("event-details", kwargs={"pk": event_a.id})

        post_data = {
            "client": client_b.id,
            "contract": contract_a.id,
            "support_contact": support_user_b.id,
            "event_status": "ended",
            "attendees": 10000,
            "event_date": datetime(2022, 9, 17).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
            "notes": "[PUT] Event Test",
        }

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.put(path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=support_user_a)
        response = api_client.put(path, post_data)
        content = response.content.decode()
        data_to_compare = {
            key: value for key, value in json.loads(content).items() if key != "id"
        }
        event_id = json.loads(content)["id"]
        assert response.status_code == 200
        assert data_to_compare == post_data
        assert event_id == event_a.id

        response = api_client.put(path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 404
        assert detail_message == "Pas trouvé."

        post_data = {
            "client": client_a.id,
            "contract": contract_a.id,
            "support_contact": support_user_a.id,
            "event_status": "ongoing",
            "attendees": 100,
            "event_date": datetime(2022, 9, 20).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
            "notes": "[PUT - management] Event Test",
        }

        api_client.force_authenticate(user=management_user)
        response = api_client.put(path, post_data)
        content = response.content.decode()
        data_to_compare = {
            key: value for key, value in json.loads(content).items() if key != "id"
        }
        event_id = json.loads(content)["id"]
        assert response.status_code == 200
        assert data_to_compare == post_data
        assert event_id == event_a.id

        api_client.force_authenticate(user=None)

    def test_update_event_patch_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        support_user_a = crm["support_user_a"]
        support_user_b = crm["support_user_b"]
        management_user = crm["management_user"]
        client_a = crm["client_a"]
        client_b = crm["client_b"]
        event_a = crm["event_a"]

        serial_event_a = copy.deepcopy(crm["serial_event_a"])
        serial_event_a["client"] = client_b.id
        serial_event_a["support_contact"] = support_user_b.id
        serial_event_a["attendees"] = 5000

        path = reverse("event-details", kwargs={"pk": event_a.id})

        patch_data = {
            "client": client_b.id,
            "support_contact": support_user_b.id,
            "attendees": 5000,
        }

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=support_user_a)
        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        data = json.loads(content)
        assert response.status_code == 200
        assert data == serial_event_a

        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 404
        assert detail_message == "Pas trouvé."

        patch_data = {
            "client": client_a.id,
            "support_contact": support_user_a.id,
            "attendees": 1000,
        }

        serial_event_a["client"] = client_a.id
        serial_event_a["support_contact"] = support_user_a.id
        serial_event_a["attendees"] = 1000

        api_client.force_authenticate(user=management_user)
        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        data = json.loads(content)
        assert response.status_code == 200
        assert data == serial_event_a

        api_client.force_authenticate(user=None)

    def test_forbidden_routes(self, api_client, crm):
        superuser = crm["superuser"]
        support_user_b = crm["support_user_b"]
        client_b = crm["client_b"]
        event_a = crm["event_a"]

        post_data = {
            "client": client_b.id,
            "support_contact": support_user_b.id,
            "event_status": "ended",
            "attendees": 10000,
            "event_date": datetime(2022, 9, 17).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
            "notes": "[PUT] Event Test",
        }

        api_client.force_authenticate(user=superuser)
        response = api_client.put(self.event_path, post_data)
        assert response.status_code == 405

        response = api_client.patch(self.event_path, post_data)
        assert response.status_code == 405

        response = api_client.delete(self.event_path)
        assert response.status_code == 405

        path = reverse("event-details", kwargs={"pk": event_a.id})

        response = api_client.post(path, post_data)
        assert response.status_code == 405

        response = api_client.delete(path)
        assert response.status_code == 405

        api_client.force_authenticate(user=None)
