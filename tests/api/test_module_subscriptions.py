import contextlib
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from app.dependencies import get_abc_service_handler
from app.doc_upstream_services.abc_api_service import AbcAPIService
from tests.conftest import HPOTTER_CREDENTIALS, build_dummy_response


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
            mock_abc.get_student_info = Mock(
                return_value=mock_response
            )  # # TODO: FAKE get student info
            return mock_abc

        app.dependency_overrides[
            get_abc_service_handler
        ] = get_abc_service_handler_override
        yield TestClient(app)

    return _abc_patched_client_fixture


def test_student_can_get_subscribed_modules(abc_patched_client, enrolment_factory):
    enrolment = enrolment_factory(student_username="hpotter")
    with abc_patched_client() as client:
        res = client.get(
            f"/{enrolment.year}/selected-modules", auth=HPOTTER_CREDENTIALS
        )
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0] == enrolment.module_code


def test_student_can_submit_valid_module_selection(abc_patched_client, session):
    module_codes = [
        {"module_code": m} for m in ["70017", "77701", "90012", "90210", "77001"]
    ]

    with abc_patched_client() as client:
        res = client.post(
            f"/{2223}/selected-modules",
            auth=HPOTTER_CREDENTIALS,
            json=module_codes,
        )

    assert res.status_code == 200
    assert len(res.json()) == 5

    enrolment_module_codes = [enrolment["module_code"] for enrolment in res.json()]

    assert enrolment_module_codes == [module["module_code"] for module in module_codes]


def test_student_cannot_select_invalid_module_selection(client):
    with client:
        res = client.post(
            f"/{2223}/selected-modules",
            auth=HPOTTER_CREDENTIALS,
            json=[],
        )

    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid Module Selection."
