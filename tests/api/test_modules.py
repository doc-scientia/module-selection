from sqlmodel import select

from app.schemas import Enrolment
from tests.conftest import HPOTTER_CREDENTIALS


def test_student_can_get_subscribed_modules(client, module_factory, enrolment_factory):
    module = module_factory()
    enrolment_factory(module=module.id, student_username="hpotter")
    with client:
        res = client.get(f"/{module.year}/subscribed_modules", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0] == module.module_code


def test_student_can_select_valid_module_selection(client, module_factory, session):
    modules = module_factory.create_batch(size=5)
    module_codes = [m.module_code for m in modules]

    with client:
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


def test_all_modules_for_year_can_be_retrieved(client, module_factory):
    modules = module_factory.create_batch(size=10, year="2223")
    with client:
        res = client.get(f"/{2223}/all_modules", auth=HPOTTER_CREDENTIALS)

    assert res.status_code == 200
    assert len(res.json()) == 10
    assert [m["module_code"] for m in res.json()] == [m.module_code for m in modules]
