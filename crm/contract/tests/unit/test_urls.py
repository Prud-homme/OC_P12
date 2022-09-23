from django.urls import resolve, reverse


def test_contract_url():
    path = reverse("contract", kwargs={})

    assert path == "/api/v1/contract/"
    assert resolve(path).view_name == "contract"


def test_contract_details_url():
    path = reverse("contract-details", kwargs={"pk": 1})

    assert path == "/api/v1/contract/1/"
    assert resolve(path).view_name == "contract-details"
