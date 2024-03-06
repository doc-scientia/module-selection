from tests.conftest import HPOTTER_CREDENTIALS


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
    client, external_module_on_offer_factory
):
    external_module = external_module_on_offer_factory()
    res = client.post(
        f"me/{external_module.year}/external-modules/choices",
        json={"module_code": external_module.code},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    assert res.json()["external_module"]["id"] == external_module.id


def test_student_cannot_apply_to_non_existing_external_module(client):
    res = client.post(
        "me/2324/external-modules/choices",
        json={"module_code": "PHY263"},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "External module with code 'PHY263' not found."


def test_student_cannot_apply_if_application_already_exists(
    client, external_module_on_offer_factory
):
    external_module = external_module_on_offer_factory(
        with_applications=[dict(username="hpotter")]
    )
    res = client.post(
        f"me/{external_module.year}/external-modules/choices",
        json={"module_code": external_module.code},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "You have already applied for this module."
