import contextlib
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from app.dependencies import get_abc_service_handler
from app.doc_upstream_services.abc_api_service import AbcAPIService
from tests.conftest import (
    ADUMBLE_CREDENTIALS,
    HPOTTER_CREDENTIALS,
    build_dummy_response,
)


@pytest.fixture(name="abc_patched_client")
def abc_patched_client_fixture(app):
    @contextlib.contextmanager
    def _abc_patched_client_fixture(
        content: dict | list[dict] | None = None, status=200
    ):
        _content = content if content is not None else [{"login": "adumble"}]

        def get_abc_service_handler_override():
            mock_abc = Mock(AbcAPIService)
            mock_response = build_dummy_response(_content, status)
            mock_abc.get_staff_info = Mock(return_value=mock_response)
            return mock_abc

        app.dependency_overrides[
            get_abc_service_handler
        ] = get_abc_service_handler_override
        yield TestClient(app)

    return _abc_patched_client_fixture


def test_staff_can_get_all_pt_meetings(
    personal_tutoring_meeting_factory, abc_patched_client
):
    personal_tutoring_meeting_factory.create_batch(size=3, year="2223")

    with abc_patched_client() as client:
        res = client.get("/2223/pt-meetings", auth=ADUMBLE_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_returns_403_if_not_staff(abc_patched_client):
    with abc_patched_client(content=[]) as client:
        res = client.get("/2324/pt-meetings", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 403
    assert res.json()["detail"] == "You cannot access this resource."


def test_returns_403_if_abc_fails(abc_patched_client):
    with abc_patched_client(status=500) as client:
        res = client.get("/2324/pt-meetings", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 403
    assert (
        res.json()["detail"]
        == "The downstream ABC service returned an invalid response. You cannot access this resource at this time."
    )
