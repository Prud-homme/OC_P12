import copy
import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestClient:

    client_path = reverse("client", kwargs={})

    def test_create_client_post_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        support_user_a = crm["support_user_a"]
        management_user = crm["management_user"]

        post_data = {
            "firstname": "John Jr",
            "lastname": "Doe",
            "email": "johnjrdoe@example.com",
            "phone": "0000000000",
            "mobile": "0000000000",
            "company_name": "Example",
            "sales_contact": sales_user_a.id,
            "obtained_with_sales_contact": sales_user_a.id,
            "client_status": "existing",
        }

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.post(self.client_path, post_data)
        content = response.content.decode()
        data_to_compare = {
            key: value
            for key, value in json.loads(content).items()
            if key in post_data.keys()
        }
        assert response.status_code == 201
        assert post_data == data_to_compare

        api_client.force_authenticate(user=support_user_a)
        response = api_client.post(self.client_path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=management_user)
        response = api_client.post(self.client_path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=None)

    def test_read_client_get_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        sales_user_b = crm["sales_user_b"]
        support_user_a = crm["support_user_a"]
        support_user_b = crm["support_user_b"]
        management_user = crm["management_user"]
        client_a = crm["client_a"]
        serial_client_a = crm["serial_client_a"]

        path = reverse("client-details", kwargs={"pk": client_a.id})

        api_client.force_authenticate(user=support_user_a)
        response = api_client.get(path)
        content = response.content.decode()
        compared_data = [
            serial_client_a[key] == value
            for key, value in json.loads(content).items()
            if key not in ["contract_client", "event_client"]
        ]
        assert response.status_code == 200
        assert False not in compared_data

        api_client.force_authenticate(user=support_user_b)
        response = api_client.get(path)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 404
        assert detail_message == "Pas trouvé."

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.get(path)
        content = response.content.decode()
        compared_data = [
            serial_client_a[key] == value
            for key, value in json.loads(content).items()
            if key not in ["contract_client", "event_client"]
        ]
        assert response.status_code == 200
        assert False not in compared_data

        api_client.force_authenticate(user=sales_user_b)
        response = api_client.get(path)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 404
        assert detail_message == "Pas trouvé."

        api_client.force_authenticate(user=management_user)
        response = api_client.get(path)
        content = response.content.decode()
        compared_data = [
            serial_client_a[key] == value
            for key, value in json.loads(content).items()
            if key not in ["contract_client", "event_client"]
        ]
        assert response.status_code == 200
        assert False not in compared_data

        response = api_client.get(self.client_path)
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 3

        response = api_client.get(self.client_path + "?email=janedoe@example.com")
        content = response.content.decode()
        count = json.loads(content)["count"]
        email = json.loads(content)["results"][0]["email"]
        assert response.status_code == 200
        assert count == 1
        assert email == "janedoe@example.com"

        response = api_client.get(self.client_path + "?email=jagrnedoe@example.com")
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 0

        response = api_client.get(self.client_path + "?lastname=Irving")
        content = response.content.decode()
        count = json.loads(content)["count"]

        assert response.status_code == 200
        assert count == 1

        response = api_client.get(self.client_path + "?lastname=ddoe")
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 0

        response = api_client.get(
            self.client_path + "?email=janedoe@example.com&lastname=doe"
        )
        content = response.content.decode()
        count = json.loads(content)["count"]
        assert response.status_code == 200
        assert count == 1

        response = api_client.get(self.client_path + "?title=janedoe@example.com")
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 400
        assert detail_message == "Le(s) filtre(s) n'existe(nt) pas"

        api_client.force_authenticate(user=None)

    def test_update_client_put_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        sales_user_b = crm["sales_user_b"]
        support_user_a = crm["support_user_a"]
        management_user = crm["management_user"]
        client_a = crm["client_a"]

        path = reverse("client-details", kwargs={"pk": client_a.id})

        post_data = {
            "firstname": "Monsieur",
            "lastname": "Dupont",
            "email": "mrdupont@example.com",
            "phone": "0000000001",
            "mobile": "0000000001",
            "company_name": "ExampleD",
            "sales_contact": sales_user_b.id,
            "obtained_with_sales_contact": sales_user_b.id,
            "client_status": "existing",
        }

        api_client.force_authenticate(user=support_user_a)
        response = api_client.put(path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.put(path, post_data)
        content = response.content.decode()
        compared_data = [
            post_data[key] == value
            for key, value in json.loads(content).items()
            if key not in ["id", "contract_client", "event_client"]
        ]
        client_id = json.loads(content)["id"]
        assert response.status_code == 200
        assert False not in compared_data
        assert client_id == client_a.id

        response = api_client.put(path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 404
        assert detail_message == "Pas trouvé."

        post_data = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "johndoe@example.com",
            "phone": "0000000000",
            "mobile": "0000000000",
            "company_name": "Example",
            "sales_contact": sales_user_a.id,
            "obtained_with_sales_contact": sales_user_a.id,
            "client_status": "existing",
        }

        api_client.force_authenticate(user=management_user)
        response = api_client.put(path, post_data)
        content = response.content.decode()
        compared_data = [
            post_data[key] == value
            for key, value in json.loads(content).items()
            if key not in ["id", "contract_client", "event_client"]
        ]
        client_id = json.loads(content)["id"]
        assert response.status_code == 200
        assert False not in compared_data
        assert client_id == client_a.id

        api_client.force_authenticate(user=None)

    def test_update_client_patch_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        sales_user_b = crm["sales_user_b"]
        support_user_a = crm["support_user_a"]
        management_user = crm["management_user"]
        client_a = crm["client_a"]

        serial_client_a = copy.deepcopy(crm["serial_client_a"])
        serial_client_a["firstname"] = "Monsieur"
        serial_client_a["lastname"] = "Dupont"
        serial_client_a["email"] = "mrdupont@example.com"
        serial_client_a["sales_contact"] = sales_user_b.id

        path = reverse("client-details", kwargs={"pk": client_a.id})

        patch_data = {
            "firstname": "Monsieur",
            "lastname": "Dupont",
            "email": "mrdupont@example.com",
            "sales_contact": sales_user_b.id,
        }

        api_client.force_authenticate(user=support_user_a)
        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        compared_data = [
            serial_client_a[key] == value
            for key, value in json.loads(content).items()
            if key not in ["contract_client", "event_client"]
        ]
        assert response.status_code == 200
        assert False not in compared_data

        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 404
        assert detail_message == "Pas trouvé."

        patch_data = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "johndoe@example.com",
            "sales_contact": sales_user_a.id,
        }

        serial_client_a["firstname"] = "John"
        serial_client_a["lastname"] = "Doe"
        serial_client_a["email"] = "johndoe@example.com"
        serial_client_a["sales_contact"] = sales_user_a.id

        api_client.force_authenticate(user=management_user)
        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        compared_data = [
            serial_client_a[key] == value
            for key, value in json.loads(content).items()
            if key not in ["contract_client", "event_client"]
        ]
        assert response.status_code == 200
        assert False not in compared_data

        api_client.force_authenticate(user=None)

    def test_forbidden_routes(self, api_client, crm):
        superuser = crm["superuser"]
        sales_user_a = crm["sales_user_a"]

        post_data = {
            "firstname": "John Jr",
            "lastname": "Doe",
            "email": "johnjrdoe@example.com",
            "phone": "0000000000",
            "mobile": "0000000000",
            "company_name": "Example",
            "sales_contact": sales_user_a.id,
        }

        api_client.force_authenticate(user=superuser)
        response = api_client.put(self.client_path, post_data)
        assert response.status_code == 405

        response = api_client.patch(self.client_path, post_data)
        assert response.status_code == 405

        response = api_client.delete(self.client_path)
        assert response.status_code == 405

        client_a = crm["client_a"]
        path = reverse("client-details", kwargs={"pk": client_a.id})

        response = api_client.post(path, post_data)
        assert response.status_code == 405

        response = api_client.delete(path)
        assert response.status_code == 405

        api_client.force_authenticate(user=None)
