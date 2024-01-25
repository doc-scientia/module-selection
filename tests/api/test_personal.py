import contextlib
import datetime
import json
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


def test_can_get_all_pt_meetings_for_me(
    personal_tutoring_meeting_factory, abc_patched_client
):
    personal_tutoring_meeting_factory.create_batch(size=3, year="2223", tutor="adumble")
    personal_tutoring_meeting_factory.create_batch(size=2)

    with abc_patched_client() as client:
        res = client.get("/me/2223/pt-meetings", auth=ADUMBLE_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_can_create_new_pt_meeting(abc_patched_client):
    payload = {
        "tutee": "xx123",
        "meeting_date": "2023-11-02",
        "label": "This is a new meeting",
    }

    with abc_patched_client() as client:
        res = client.post(
            "/me/2324/pt-meetings", json=payload, auth=ADUMBLE_CREDENTIALS
        )
    assert res.status_code == 200
    meeting = res.json()
    assert meeting["tutee"] == "xx123"
    assert meeting["year"] == "2324"
    assert meeting["tutor"] == "adumble"
    assert meeting["label"] == "This is a new meeting"


@pytest.mark.parametrize(
    "method, url",
    [
        ("get", "/me/2324/pt-meetings"),
        ("post", "/me/2324/pt-meetings"),
    ],
)
def test_returns_403_if_not_staff(method, url, abc_patched_client):
    with abc_patched_client(content=[]) as client:
        res = getattr(client, method)(url, auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 403
    assert res.json()["detail"] == "You cannot access this resource."


@pytest.mark.parametrize(
    "method, url",
    [
        ("get", "/me/2324/pt-meetings"),
        ("post", "/me/2324/pt-meetings"),
    ],
)
def test_returns_403_if_abc_fails(method, url, abc_patched_client):
    with abc_patched_client(status=500) as client:
        res = getattr(client, method)(url, auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 403
    assert (
        res.json()["detail"]
        == "The downstream ABC service returned an invalid response. You cannot access this resource at this time."
    )


def test_staff_delete_other_tutor_meeting(
    abc_patched_client,
    personal_tutoring_meeting_factory,
):
    meeting = personal_tutoring_meeting_factory(year="2223", tutor="hpotter")
    with abc_patched_client() as client:
        res = client.delete(
            f"/me/2223/pt-meetings/{meeting.id}", auth=ADUMBLE_CREDENTIALS
        )

    assert res.status_code == 403
    assert res.json()["detail"] == "Not authorized to delete this meeting"


def test_tutor_can_delete_own_meeting(
    abc_patched_client,
    personal_tutoring_meeting_factory,
):
    meeting = personal_tutoring_meeting_factory(year="2223", tutor="adumble")
    with abc_patched_client() as client:
        res = client.delete(
            f"/me/2223/pt-meetings/{meeting.id}", auth=ADUMBLE_CREDENTIALS
        )

    assert res.status_code == 204


def test_cannot_delete_non_existing_meeting(abc_patched_client):
    with abc_patched_client() as client:
        res = client.delete(f"/me/2223/pt-meetings/{1}", auth=ADUMBLE_CREDENTIALS)

    assert res.status_code == 404


def test_staff_cannot_edit_other_tutor_meeting(
    personal_tutoring_meeting_factory, abc_patched_client
):
    meeting = personal_tutoring_meeting_factory(year="2223", tutor="hpotter")
    payload = json.dumps({"meeting_date": str(datetime.date.today()), "label": "New"})

    with abc_patched_client() as client:
        res = client.put(
            f"/me/2223/pt-meetings/{meeting.id}", json=payload, auth=ADUMBLE_CREDENTIALS
        )

    assert res.status_code == 403
    assert res.json()["detail"] == "Not authorized to delete this meeting"


def test_tutor_can_edit_own_meeting(
    abc_patched_client,
    personal_tutoring_meeting_factory,
):
    meeting = personal_tutoring_meeting_factory(
        year="2223",
        tutor="adumble",
        label="Original",
        meeting_date=datetime.datetime.now() - datetime.timedelta(weeks=2),
    )

    NEW_DATE = str(datetime.date(2023, 10, 10))
    NEW_LABEL = "New"

    payload = {"meeting_date": NEW_DATE, "label": NEW_LABEL}

    with abc_patched_client() as client:
        res = client.put(
            f"/me/2223/pt-meetings/{meeting.id}", json=payload, auth=ADUMBLE_CREDENTIALS
        )

    assert res.status_code == 200
    assert res.json()["meeting_date"] == NEW_DATE
    assert res.json()["label"] == NEW_LABEL


def test_cannot_edit_non_existing_meeting(abc_patched_client):
    with abc_patched_client() as client:
        res = client.put("/me/2223/pt-meetings/1", json={}, auth=ADUMBLE_CREDENTIALS)

    assert res.status_code == 404


def test_gets_no_sessions_if_no_attendance_for_user_exists(
    client, tutoring_session_factory
):
    existing_session = tutoring_session_factory()

    res = client.get(f"/me/{existing_session.year}/sessions", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_can_get_all_personal_sessions(client, tutoring_session_factory):
    existing_session = tutoring_session_factory(
        with_attendances=[{"username": HPOTTER_CREDENTIALS.username, "present": True}]
    )

    res = client.get(f"/me/{existing_session.year}/sessions", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 1
    [session] = res.json()
    assert session["group"] == existing_session.group
    assert session["date"] == existing_session.date.strftime("%Y-%m-%d")
    assert session["id"] == existing_session.id
    assert session["present"] is True
