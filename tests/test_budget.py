from starlette.testclient import TestClient


def test_get_user_budget(fixture_app, logged_user_credentials):
    with TestClient(fixture_app) as client:
        response = client.get("v1/users/budgets", headers={**logged_user_credentials})
        assert response.status_code == 200

        resp_json = response.json()
        assert resp_json.get("items")
        assert resp_json["items"][0]["title"] == "school"


def test_user_create_budget(fixture_app, logged_user_credentials):
    with TestClient(fixture_app) as client:
        data = {
            "title": "Car budget",
            "description": "Money for car",
            "amount": 2000,
            "category_id": "14b651ce-d7d5-46b5-b66f-db5a7b29d640",
            "created_by_id": "e16683f2-4bcb-4bdf-812b-1a2bae7de22d",
        }
        response = client.post(
            "v1/budgets/create",
            json=data,
            headers={**logged_user_credentials},
        )
        assert response.status_code == 200

        resp_json = response.json()
        assert resp_json.get("title") == data["title"]


def test_user_share_budget(fixture_app, logged_user_credentials):
    with TestClient(fixture_app) as client:
        data = {
            "budget_id": "4bd784ad-f73a-4955-b8cf-99f3aa7020ad",
            "user_ids": ["091dd9a4-a641-4886-b06d-00498220e610"],
            "message": "Shared budget",
            "description": "yooo",
        }

        response = client.post(
            "v1/users/share-budget",
            json=data,
            headers={**logged_user_credentials},
        )
        assert response.status_code == 200

        resp_json = response.json()
        assert resp_json.get("shared_budget")
