from starlette.testclient import TestClient


def test_create_expenses(fixture_app, logged_user_credentials):
    with TestClient(fixture_app) as client:
        data = {
            "operation_type": "outcomes",
            "budget_id": "4bd784ad-f73a-4955-b8cf-99f3aa7020ad",
            "amount": 100,
            "commentary": "ice cream",
            "title": "ice cream",
            "created_by_id": "e16683f2-4bcb-4bdf-812b-1a2bae7de22d",
        }
        response = client.post(
            "v1/operations/create-operation",
            json=data,
            headers={**logged_user_credentials},
        )
        assert response.status_code == 200

        response = client.get(
            "v1/users/budgets",
            headers={**logged_user_credentials},
        )

        assert response.status_code == 200
        resp_json = response.json()

        assert resp_json["items"][0]["amount"] == 900
