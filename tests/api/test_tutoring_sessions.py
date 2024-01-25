import contextlib
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from app.dependencies import get_abc_service_handler
from app.doc_upstream_services.abc_api_service import AbcAPIService
from tests.conftest import HPOTTER_CREDENTIALS, build_dummy_response

payload = {
    "group": "PMT 2",
    "date": "2023-11-02",
    "attendances": [{"username": "hpotter", "present": False}],
}


@pytest.fixture(name="abc_patched_client")
def abc_patched_client_fixture(app):
    default_response = [{"tutor": {"login": "adumble"}, "uta": {"login": "hpotter"}}]

    @contextlib.contextmanager
    def _abc_patched_client_fixture(
        content: dict | list[dict] | None = None, status=200
    ):
        _content = content if content is not None else default_response

        def get_abc_service_handler_override():
            mock_abc = Mock(AbcAPIService)
            mock_response = build_dummy_response(_content, status)
            mock_abc.get_tutorial_groups = Mock(return_value=mock_response)
            return mock_abc

        app.dependency_overrides[
            get_abc_service_handler
        ] = get_abc_service_handler_override
        yield TestClient(app)

    return _abc_patched_client_fixture


@pytest.mark.parametrize(
    "method, url",
    [
        ("get", "/2122/sessions"),
        ("post", "/2122/sessions"),
        ("put", "/2122/sessions/1"),
        ("delete", "/2122/sessions/1"),
    ],
)
def test_returns_403_if_not_tutor_nor_uta(method, url, abc_patched_client):
    with abc_patched_client([{"tutor": {"login": "adumble"}, "uta": None}]) as client:
        res = getattr(client, method)(url, auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 403
    assert res.json()["detail"] == "You cannot access this resource."


def test_can_get_all_existing_sessions_for_year(
    tutoring_session_factory, abc_patched_client
):
    session = tutoring_session_factory(with_attendances=2)

    with abc_patched_client() as client:
        res = client.get(f"/{session.year}/sessions", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 1
    [session] = res.json()
    assert len(session["attendances"]) == 2


def test_can_filter_existing_sessions_by_group(
    tutoring_session_factory, abc_patched_client
):
    tutoring_session_factory(year="2122", group="PPT 1")
    tutoring_session_factory(year="2122")
    with abc_patched_client() as client:
        res = client.get(
            "/2122/sessions", params=dict(group="PPT 1"), auth=HPOTTER_CREDENTIALS
        )
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_can_create_new_session(abc_patched_client):
    with abc_patched_client() as client:
        res = client.post("/2122/sessions", json=payload, auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    session = res.json()
    assert session["id"] is not None
    assert session["group"] == payload["group"]
    assert session["date"] == payload["date"]
    assert session["year"] == "2122"
    assert len(session["attendances"]) == 1
    [attendance] = session["attendances"]
    payload_attendance = payload["attendances"][0]
    assert attendance["id"] is not None
    assert attendance["username"] == payload_attendance["username"]
    assert attendance["present"] == payload_attendance["present"]


def test_cannot_update_non_existing_session(abc_patched_client):
    with abc_patched_client() as client:
        res = client.put("/2122/sessions/1", json=payload, auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 404
    assert res.json()["detail"] == "Tutoring session not found."


def test_can_update_existing_session(tutoring_session_factory, abc_patched_client):
    existing_session = tutoring_session_factory(with_attendances=2)
    previous_date = existing_session.date
    payload = {
        "group": existing_session.group,
        "date": "2023-11-02",
        "attendances": [{"username": "hpotter", "present": False}],
    }
    with abc_patched_client() as client:
        res = client.put(
            f"/{existing_session.year}/sessions/{existing_session.id}",
            json=payload,
            auth=HPOTTER_CREDENTIALS,
        )
    assert res.status_code == 200
    session = res.json()
    assert session["id"] == existing_session.id
    assert session["group"] == existing_session.group
    assert session["year"] == existing_session.year
    assert session["date"] != previous_date.strftime("%Y-%m-%d")
    assert session["date"] == payload["date"]
    assert len(session["attendances"]) == 1


def test_can_delete_existing_session(tutoring_session_factory, abc_patched_client):
    existing_session = tutoring_session_factory(with_attendances=2)
    with abc_patched_client() as client:
        res = client.delete(
            f"/{existing_session.year}/sessions/{existing_session.id}",
            auth=HPOTTER_CREDENTIALS,
        )
    assert res.status_code == 204
    assert not res.content
