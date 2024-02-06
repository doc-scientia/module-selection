import contextlib
from unittest.mock import Mock

import pytest
from sqlmodel import select
from starlette.testclient import TestClient

from app.dependencies import get_abc_service_handler
from app.doc_upstream_services.abc_api_service import AbcAPIService
from app.schemas import Enrolment
from tests.conftest import HPOTTER_CREDENTIALS
from tests.conftest import build_dummy_response


# TODO: CREATE FIXTURE abc_patched_client
@pytest.fixture(name="abc_patched_client")
def abc_patched_client_fixture(app):
    @contextlib.contextmanager
    def _abc_patched_client_fixture(
            content: dict | list[dict] | None = None, status=200
    ):
        _content = content if content is not None else [{"login": "hpotter"}]

        def get_abc_service_handler_override():
            mock_abc = Mock(AbcAPIService)
            mock_response = build_dummy_response(_content, status)
            mock_abc.get_student_info = Mock(return_value=mock_response)  # # TODO: FAKE get student info
            return mock_abc

        app.dependency_overrides[
            get_abc_service_handler
        ] = get_abc_service_handler_override
        yield TestClient(app)

    return _abc_patched_client_fixture


def test_student_can_get_subscribed_modules(abc_patched_client, module_factory, enrolment_factory):
    module = module_factory()
    enrolment_factory(module=module.id, student_username="hpotter")
    with  abc_patched_client() as client:
        res = client.get(f"/{module.year}/subscribed_modules", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0] == module.module_code


def test_student_can_submit_valid_module_selection(abc_patched_client, module_factory, session):
    modules = module_factory.create_batch(size=5)
    module_codes = [m.module_code for m in modules]

    with abc_patched_client() as client:
        res = client.post(
            f"/{2223}/subscribed_modules",
            auth=HPOTTER_CREDENTIALS,
            json={"module_codes": module_codes},
        )

    assert res.status_code == 200
    assert res.json() == module_codes

    query = select(Enrolment).where(Enrolment.student_username == "hpotter")
    new_enrolment_module_ids = [
        new_enrolment.module for new_enrolment in session.exec(query).all()
    ]

    assert new_enrolment_module_ids == [module.id for module in modules]


def test_student_cannot_select_invalid_module_selection(client):
    modules = []
    with client:
        res = client.post(
            f"/{2223}/subscribed_modules",
            auth=HPOTTER_CREDENTIALS,
            json={"module_codes": modules},
        )

    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid Module Selection."
