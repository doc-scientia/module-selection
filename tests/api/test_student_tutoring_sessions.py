from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from app.dependencies import get_abc_service_handler
from app.doc_upstream_services.abc_api_service import AbcAPIService
from tests.conftest import HPOTTER_CREDENTIALS, build_dummy_response


@pytest.fixture(name="abc_patched_client")
def abc_patched_client_fixture(app):
    def get_abc_service_handler_override():
        tutorial_group_content = [
            {"tutor": {"login": "cdiggory"}, "uta": {"login": None}}
        ]
        tutorial_group_response = build_dummy_response(tutorial_group_content)
        staff_info_response = build_dummy_response([])
        mock_abc = Mock(AbcAPIService)
        mock_abc.get_tutorial_groups = Mock(return_value=tutorial_group_response)
        mock_abc.get_staff_info = Mock(return_value=staff_info_response)
        return mock_abc

    app.dependency_overrides[get_abc_service_handler] = get_abc_service_handler_override
    yield TestClient(app)


def test_returns_403_if_not_matching_student_nor_tutor_nor_uta(abc_patched_client):
    res = abc_patched_client.get(
        "/2324/rweasley/tutoring-sessions", auth=HPOTTER_CREDENTIALS
    )
    assert res.status_code == 403
    assert res.json()["detail"] == "You cannot access this resource."


def test_student_can_get_their_own_tutoring_sessions(client, tutoring_session_factory):
    tutoring_session_factory.create_batch(
        size=3, year="2324", with_attendances=[dict(username="hpotter")]
    )
    res = client.get("/2324/hpotter/tutoring-sessions", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 3
