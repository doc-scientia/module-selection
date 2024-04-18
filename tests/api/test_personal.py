import contextlib
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from pydantic import BaseModel
from starlette.testclient import TestClient

from app.dependencies.main import get_abc_service_handler
from app.doc_upstream_services.abc.api_service import AbcAPIService
from app.doc_upstream_services.abc.deserialisation import S
from app.schemas.configurations import ModuleSelectionStatus
from tests.conftest import HPOTTER_CREDENTIALS


class TestStudent(BaseModel):
    degree_year: str


@pytest.fixture(name="abc_patched_client")
def abc_patched_client_fixture(app):
    @contextlib.contextmanager
    def _abc_patched_client_fixture(method: str, content: type[S]):
        def get_abc_service_handler_override():
            mock_abc = Mock(AbcAPIService)
            setattr(mock_abc, method, Mock(return_value=content))
            return mock_abc

        app.dependency_overrides[
            get_abc_service_handler
        ] = get_abc_service_handler_override
        yield TestClient(app)

    return _abc_patched_client_fixture


@pytest.fixture(name="open_module_selection")
def open_module_selection_fixture(request, configuration_factory):
    @contextlib.contextmanager
    def _open_module_selection(year: str):
        if "no_autouse" not in request.keywords:
            now = datetime.utcnow()
            yield configuration_factory(
                status=ModuleSelectionStatus.USE_PERIODS,
                year=year,
                with_periods=[
                    dict(start=now - timedelta(days=1), end=now + timedelta(days=1))
                ],
            )

    return _open_module_selection


def test_student_can_get_own_external_module_choices(
    client, external_module_on_offer_factory
):
    external_module_on_offer_factory.create_batch(
        size=3, year="2324", with_applications=[dict(username="hpotter")]
    )
    res = client.get(
        "me/2324/external-modules/choices",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_student_can_submit_valid_external_module_registration(
    client, external_module_on_offer_factory, open_module_selection
):
    external_module = external_module_on_offer_factory()
    with open_module_selection(external_module.year):
        res = client.post(
            f"me/{external_module.year}/external-modules/choices",
            json={"module_code": external_module.code},
            auth=HPOTTER_CREDENTIALS,
        )
    assert res.status_code == 200
    assert res.json()["external_module_id"] == external_module.id


def test_student_cannot_apply_to_non_existing_external_module(
    client, open_module_selection
):
    with open_module_selection("2324"):
        res = client.post(
            "me/2324/external-modules/choices",
            json={"module_code": "PHY263"},
            auth=HPOTTER_CREDENTIALS,
        )
    assert res.status_code == 404
    assert res.json()["detail"] == "External module with code 'PHY263' not found."


def test_student_cannot_apply_if_application_already_exists(
    client, external_module_on_offer_factory, open_module_selection
):
    external_module = external_module_on_offer_factory(
        with_applications=[dict(username="hpotter")]
    )
    with open_module_selection(external_module.year):
        res = client.post(
            f"me/{external_module.year}/external-modules/choices",
            json={"module_code": external_module.code},
            auth=HPOTTER_CREDENTIALS,
        )
    assert res.status_code == 400
    assert res.json()["detail"] == "You have already applied for this module."


def test_student_can_get_own_internal_module_choices(
    client, internal_module_on_offer_factory
):
    internal_module_on_offer_factory.create_batch(
        size=3,
        year="2324",
        with_regulations=[dict(with_enrollments=[dict(username="hpotter")])],
    )
    res = client.get(
        "me/2324/internal-modules/choices",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_student_can_select_valid_internal_module(
    abc_patched_client,
    degree_ects_constraints_factory,
    internal_module_on_offer_factory,
    offering_group_factory,
    open_module_selection,
):
    degree_constraints = degree_ects_constraints_factory()
    offering_group = offering_group_factory(degree=degree_constraints.degree)
    internal_module = internal_module_on_offer_factory(
        year=degree_constraints.degree,
        with_regulations=[
            dict(
                degree=degree_constraints.degree,
                offering_group=offering_group,
                ects=offering_group.min,
            )
        ],
    )

    with open_module_selection(internal_module.year):
        with abc_patched_client(
            content=TestStudent(degree_year=degree_constraints.degree),
            method="get_student",
        ) as client:
            res = client.post(
                f"me/{internal_module.year}/internal-modules/choices",
                json={
                    "module_code": internal_module.code,
                    "degree": degree_constraints.degree,
                },
                auth=HPOTTER_CREDENTIALS,
            )
    assert res.status_code == 200
    assert res.json()["degree_regulations"]["degree"] == degree_constraints.degree
    assert res.json()["degree_regulations"]["module_id"] == internal_module.id


def test_student_cannot_select_module_if_selection_violates_offering_group_constraint(
    abc_patched_client,
    internal_module_on_offer_factory,
    offering_group_factory,
    open_module_selection,
):
    degree = "mc3"
    offering_group = offering_group_factory()
    internal_module_on_offer_factory(
        year=offering_group.year,
        with_regulations=[
            dict(
                degree=degree,
                offering_group=offering_group,
                ects=offering_group.max,
                with_enrollments=[dict(username=HPOTTER_CREDENTIALS.username)],
            )
        ],
    )
    internal_module = internal_module_on_offer_factory(
        year=offering_group.year,
        with_regulations=[dict(degree=degree, offering_group=offering_group)],
    )

    with open_module_selection(internal_module.year):
        with abc_patched_client(
            content=TestStudent(degree_year=degree), method="get_student"
        ) as client:
            res = client.post(
                f"me/{internal_module.year}/internal-modules/choices",
                json={"module_code": internal_module.code, "degree": degree},
                auth=HPOTTER_CREDENTIALS,
            )
    assert res.status_code == 400
    assert (
        res.json()["detail"]
        == f"Your selection violates the maximum number of ects for {offering_group.label}."
    )


def test_student_cannot_select_non_existing_internal_module(
    abc_patched_client, open_module_selection
):
    with open_module_selection("2324"):
        with abc_patched_client(
            content=TestStudent(degree_year="mc3"), method="get_student"
        ) as client:
            res = client.post(
                "me/2324/internal-modules/choices",
                json={
                    "module_code": "50002",
                },
                auth=HPOTTER_CREDENTIALS,
            )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module with code '50002' not found."


def test_student_cannot_select_internal_module_if_not_offered_to_requested_degree(
    abc_patched_client, internal_module_on_offer_factory, open_module_selection
):
    internal_module = internal_module_on_offer_factory(with_regulations=1)

    with open_module_selection(internal_module.year):
        with abc_patched_client(
            content=TestStudent(degree_year="XXX"), method="get_student"
        ) as client:
            res = client.post(
                f"me/{internal_module.year}/internal-modules/choices",
                json={
                    "module_code": internal_module.code,
                },
                auth=HPOTTER_CREDENTIALS,
            )
    assert res.status_code == 400
    assert (
        res.json()["detail"]
        == f"Module with code '{internal_module.code}' not offered to degree 'XXX'."
    )


def test_student_cannot_select_internal_module_if_already_selected(
    abc_patched_client, internal_module_on_offer_factory, open_module_selection
):
    degree = "mc3"
    internal_module = internal_module_on_offer_factory(
        with_regulations=[
            dict(degree=degree, with_enrollments=[dict(username="hpotter")])
        ]
    )

    with open_module_selection(internal_module.year):
        with abc_patched_client(
            content=TestStudent(degree_year=degree), method="get_student"
        ) as client:
            res = client.post(
                f"me/{internal_module.year}/internal-modules/choices",
                json={"module_code": internal_module.code, "degree": degree},
                auth=HPOTTER_CREDENTIALS,
            )
    assert res.status_code == 400
    assert res.json()["detail"] == "You have already applied for this module."


def test_student_cannot_select_internal_module_if_module_selection_not_open(
    abc_patched_client, open_module_selection
):
    with open_module_selection("2324"):
        with abc_patched_client(
            content=TestStudent(degree_year="mc3"), method="get_student"
        ) as client:
            res = client.post(
                "me/2324/internal-modules/choices",
                json={"module_code": "50002"},
                auth=HPOTTER_CREDENTIALS,
            )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module with code '50002' not found."
