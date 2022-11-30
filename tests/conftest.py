import pytest
from alembic.config import Config
from pytest_mock import MockFixture

from tests import const
import alembic


@pytest.fixture
def mock_settings(mocker: MockFixture):
    mocker.patch("family_budget.core.config", return_value=const)


@pytest.fixture
def config():
    return const


@pytest.fixture(name="apply_migrations")
def fixture_apply_migrations():
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture
def fixture_app(
    apply_migrations,
    mock_settings
):
    from family_budget.app import get_application
    return get_application()

