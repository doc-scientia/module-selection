import json
import os
from contextlib import contextmanager
from datetime import datetime
from unittest import mock
from unittest.mock import Mock

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from requests.auth import HTTPBasicAuth
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session, SQLModel, create_engine

from app.dev_upstream_services.abc_api_service import DummyResponse
from app.doc_upstream_services.abc_api_service import AbcAPIService
from app.doc_upstream_services.response_wrappers import UpstreamResponse

TEST_DB_SERVER_URL: str = os.environ.get("TEST_DB_SERVER_URL", "postgresql://")
HPOTTER_CREDENTIALS = HTTPBasicAuth(username="hpotter", password="leviosa")
ADUMBLE_CREDENTIALS = HTTPBasicAuth(username="adumble", password="password")
ROLE_USER_CREDENTIALS = ("role_user", "role_password")

ABC_ROOT = "https://abc-api.doc.ic.ac.uk"

HARRY_POTTER = "hpotter"
HARRY_POTTER_INFO = {
    "login": "hpotter",
    "email": "harryp1@imperial.ac.uk",
    "lastname": "Potter",
    "firstname": "Harry",
    "role_in_department": "student",
    "modules": [],
}

# This one NEEDS to be set before any import from app is made
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from app import create_application, factories
from app.dependencies.main import (
    basic_auth,
    get_abc_service_handler,
    get_current_user,
    get_session,
    get_settings,
)
from app.settings import Settings

model_factories = [f for f in factories.all_factories]
for factory in model_factories:
    register(factory)


def set_session_for_factories(factory_objects, session: Session):
    for f in factory_objects:
        f._meta.sqlalchemy_session = session


@pytest.fixture(name="db_engine", scope="session")
def db_engine_fixture():
    engine = create_engine(f"{TEST_DB_SERVER_URL}/test-module_subscriptions")
    if database_exists(engine.url):
        # Catch case in which previous test run failed without teardown
        drop_database(engine.url)
    create_database(engine.url)
    SQLModel.metadata.create_all(engine)
    yield engine
    drop_database(engine.url)


@pytest.fixture(name="session", autouse=True)
def session_fixture(db_engine):
    connection = db_engine.connect()

    transaction = connection.begin()
    with Session(connection) as session:
        set_session_for_factories(model_factories, session)
        yield session
        transaction.rollback()
        connection.close()


@pytest.fixture(name="app")
def app_fixture(session: Session):
    app: FastAPI = create_application()

    def get_session_override():
        return session

    def get_settings_override():
        return Settings(testing=1)

    def get_current_user_override(token=Depends(basic_auth)):
        return token.username

    def get_abc_service_handler_override():
        return Mock(AbcAPIService)

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    app.dependency_overrides[get_abc_service_handler] = get_abc_service_handler_override

    yield app
    app.dependency_overrides.clear()


@pytest.fixture(name="app_as_user")
def app_with_pretended_authenticated_user_fixture(app: FastAPI):
    @contextmanager
    def set_current_user(username: str):
        def get_current_user_override(token=Depends(basic_auth)):
            return username

        app.dependency_overrides[get_current_user] = get_current_user_override
        yield app

    return set_current_user


@pytest.fixture(name="client")
def client_fixture(app) -> TestClient:
    return TestClient(app)


def to_datetime(formatted: str) -> datetime:
    return datetime.strptime(formatted, "%Y-%m-%dT%H:%M:%S%z")


def build_dummy_response(
    content: dict | list[dict] | None, status: int = 200
) -> UpstreamResponse:
    return UpstreamResponse(
        DummyResponse(
            status_code=status,
            content=json.dumps(content),
        )
    )
