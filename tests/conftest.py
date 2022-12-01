import os

from pytest_mock import MockFixture
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
import pytest

from alembic.config import Config
from family_budget.core.utils import get_hashed_password
from tests import const
import alembic


@pytest.fixture
def mock_settings(mocker: MockFixture):
    mocker.patch.dict(
        os.environ,
        {
            "JWT_SECRET_KEY": const.JWT_SECRET_KEY,
            "JWT_REFRESH_SECRET_KEY": const.JWT_REFRESH_SECRET_KEY,
        },
    )
    mocker.patch("family_budget.core.config.get_settings", return_value=const)


@pytest.fixture(name="apply_migrations")
def fixture_apply_migrations(mock_settings):
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture
def fixture_app(apply_migrations, mock_settings, prepare_data):
    from family_budget.app import get_application

    return get_application()


@pytest.fixture
def config():
    return const


@pytest.fixture
def prepare_data(app_test_db: Session):
    password = get_hashed_password("test_pass")
    app_test_db.execute(
        f"""
        insert into "user" 
        (id, created_at, first_name, last_name, email, phone_number, hashed_password)
        values 
        ('e16683f2-4bcb-4bdf-812b-1a2bae7de22d', '2022-10-10', 'islom', 'karimov', 'islam.karimov@mail.com', '998935271944', '{password}'),        
        ('091dd9a4-a641-4886-b06d-00498220e610', '2022-10-10', 'kamila', 'karimov', 'kamila.karimov@mail.com', '998935271944', '{password}');
        
        insert into budgetcategory (id, created_at, title, description)
        values ('14b651ce-d7d5-46b5-b66f-db5a7b29d640', '2022-10-10', 'Cool category', 'nice description');
        """
    )
    app_test_db.commit()

    app_test_db.execute(
        f"""
            insert into budget (id, created_at, title, description, amount, category_id, created_by_id)
            values ('4bd784ad-f73a-4955-b8cf-99f3aa7020ad', '2022-10-10', 'school', 'school saving money', 1000, '14b651ce-d7d5-46b5-b66f-db5a7b29d640', 'e16683f2-4bcb-4bdf-812b-1a2bae7de22d');
        """
    )
    app_test_db.commit()


@pytest.fixture
def app_test_db(mock_settings, apply_migrations):
    from family_budget.core.database import get_db_session

    return next(get_db_session())


@pytest.fixture
def logged_user_credentials(fixture_app):
    with TestClient(fixture_app) as client:
        response = client.post(
            url="v1/auth/login",
            data={"username": "islam.karimov@mail.com", "password": "test_pass"},
        )

        resp_json = response.json()
        access_token = resp_json.get("access_token")

    return {"authorization": f"Bearer {access_token}"}
