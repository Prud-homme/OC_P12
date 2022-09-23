import copy
import json
from datetime import datetime

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestContract:

    contract_path = reverse("contract", kwargs={})

    def test_contract_post_method(self, api_client, crm):
        client_a = crm["client_a"]
        sales_user_a = crm["sales_user_a"]
        support_user_a = crm["support_user_a"]
        management_user = crm["management_user"]

        post_data = {
            "sales_contact": sales_user_a.id,
            "client": client_a.id,
            "status": True,
            "amount": 1250.99,
            "payment_due": datetime(2022, 9, 15).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
        }

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.post(self.contract_path, post_data)
        content = response.content.decode()
        data_to_compare = {
            key: value for key, value in json.loads(content).items() if key != "id"
        }

        assert response.status_code == 201
        assert post_data == data_to_compare

        api_client.force_authenticate(user=support_user_a)
        response = api_client.post(self.contract_path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=management_user)
        response = api_client.post(self.contract_path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=None)

    def test_contract_get_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        sales_user_b = crm["sales_user_b"]
        support_user_a = crm["support_user_a"]
        management_user = crm["management_user"]
        contract_a = crm["contract_a"]
        serial_contract_a = crm["serial_contract_a"]

        path = reverse("contract-details", kwargs={"pk": contract_a.id})

        api_client.force_authenticate(user=support_user_a)
        response = api_client.get(path)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 403
        assert (
            detail_message == "Vous n'avez pas la permission d'effectuer cette action."
        )

        api_client.force_authenticate(user=sales_user_a)
        response = api_client.get(path)
        content = response.content.decode()
        data = json.loads(content)
        assert response.status_code == 200
        assert data == serial_contract_a

        api_client.force_authenticate(user=sales_user_b)
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
        assert data == serial_contract_a

        api_client.force_authenticate(user=None)

    def test_contract_put_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        sales_user_b = crm["sales_user_b"]
        support_user_a = crm["support_user_a"]
        management_user = crm["management_user"]
        client_a = crm["client_a"]
        client_b = crm["client_b"]
        contract_a = crm["contract_a"]

        path = reverse("contract-details", kwargs={"pk": contract_a.id})

        post_data = {
            "sales_contact": sales_user_b.id,
            "client": client_b.id,
            "status": False,
            "amount": 12000.99,
            "payment_due": datetime(2022, 9, 10).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
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
        data_to_compare = {
            key: value for key, value in json.loads(content).items() if key != "id"
        }
        contract_id = json.loads(content)["id"]
        assert response.status_code == 200
        assert data_to_compare == post_data
        assert contract_id == contract_a.id

        response = api_client.put(path, post_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 404
        assert detail_message == "Pas trouvé."

        post_data = {
            "sales_contact": sales_user_a.id,
            "client": client_a.id,
            "status": True,
            "amount": 1200.99,
            "payment_due": datetime(2022, 9, 15).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
        }

        api_client.force_authenticate(user=management_user)
        response = api_client.put(path, post_data)
        content = response.content.decode()
        data_to_compare = {
            key: value for key, value in json.loads(content).items() if key != "id"
        }
        contract_id = json.loads(content)["id"]
        assert response.status_code == 200
        assert data_to_compare == post_data
        assert contract_id == contract_a.id

        api_client.force_authenticate(user=None)

    def test_contract_patch_method(self, api_client, crm):
        sales_user_a = crm["sales_user_a"]
        sales_user_b = crm["sales_user_b"]
        support_user_a = crm["support_user_a"]
        management_user = crm["management_user"]
        client_a = crm["client_a"]
        client_b = crm["client_b"]
        contract_a = crm["contract_a"]

        serial_contract_a = copy.deepcopy(crm["serial_contract_a"])
        serial_contract_a["sales_contact"] = sales_user_b.id
        serial_contract_a["client"] = client_b.id
        serial_contract_a["status"] = False

        path = reverse("contract-details", kwargs={"pk": contract_a.id})

        patch_data = {
            "sales_contact": sales_user_b.id,
            "client": client_b.id,
            "status": False,
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
        data = json.loads(content)
        assert response.status_code == 200
        assert data == serial_contract_a

        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        detail_message = json.loads(content)["detail"]
        assert response.status_code == 404
        assert detail_message == "Pas trouvé."

        patch_data = {
            "sales_contact": sales_user_a.id,
            "client": client_a.id,
            "status": True,
        }

        serial_contract_a["sales_contact"] = sales_user_a.id
        serial_contract_a["client"] = client_a.id
        serial_contract_a["status"] = True

        api_client.force_authenticate(user=management_user)
        response = api_client.patch(path, patch_data)
        content = response.content.decode()
        data = json.loads(content)
        assert response.status_code == 200
        assert data == serial_contract_a

        api_client.force_authenticate(user=None)

    def test_forbidden_routes(self, api_client, crm):
        superuser = crm["superuser"]
        client_a = crm["client_a"]
        sales_user_a = crm["sales_user_a"]

        post_data = {
            "sales_contact": sales_user_a.id,
            "client": client_a.id,
            "status": True,
            "amount": 1250.99,
            "payment_due": datetime(2022, 9, 15).strftime(r"%Y-%m-%dT%H:%M:%SZ"),
        }

        api_client.force_authenticate(user=superuser)
        response = api_client.put(self.contract_path, post_data)
        assert response.status_code == 405

        response = api_client.patch(self.contract_path, post_data)
        assert response.status_code == 405

        response = api_client.get(self.contract_path)
        assert response.status_code == 405

        response = api_client.delete(self.contract_path)
        assert response.status_code == 405

        contract_a = crm["contract_a"]
        path = reverse("contract-details", kwargs={"pk": contract_a.id})

        response = api_client.post(path, post_data)
        assert response.status_code == 405

        response = api_client.delete(path)
        assert response.status_code == 405

        api_client.force_authenticate(user=None)
