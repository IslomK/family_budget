from fastapi.testclient import TestClient
import pytest


def test_user_not_auth(mock_settings, fixture_app):
    with TestClient(fixture_app) as client:
        response = client.get("v1/users/details")
        assert response.status_code == 401


@pytest.mark.parametrize(
    "username,password,expected1, expected2",
    (
        [
            ("islam.karimov@mail.com", "test_pass", 200, 200),
            ("test_user", "test_pass", 400, 403),
        ]
    ),
)
def test_user_login(mock_settings, fixture_app, username, password, expected1, expected2):
    with TestClient(fixture_app) as client:
        response = client.post(
            url="v1/auth/login",
            data={"username": username, "password": password},
        )
        assert response.status_code == expected1

        resp_json = response.json()
        access_token = resp_json.get("access_token")

        response = client.get(
            "v1/users/details", headers={"authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == expected2


@pytest.mark.parametrize(
    "first_name,last_name,email,password,repeat_pass,expected",
    (
        [
            ("said", "isaev", "said@isaev", "test_pass", "test_pass", 200),
            ("test", "user", "test_user@mail.com", "test_pass", "diff_pass", 422),
        ]
    ),
)
def test_user_create(fixture_app, first_name, last_name, email, password, repeat_pass, expected):
    with TestClient(fixture_app) as client:
        response = client.post(
            url="v1/users/create",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": "9993939333",
                "password": password,
                "repeat_password": repeat_pass,
            },
        )
        assert response.status_code == expected

        if expected == 200:
            resp_json = response.json()
            assert first_name == resp_json.get("first_name")
            assert email == resp_json.get("email")
