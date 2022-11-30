from fastapi.testclient import TestClient
import pytest


@pytest.mark.api
def test_healthy_healtz(fixture_app):
    with TestClient(fixture_app) as client:
        response = client.get('v1/healthcheck')
        assert response.status_code == 200