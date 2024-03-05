from tests.conftest import HPOTTER_CREDENTIALS


def test_student_can_get_own_external_module_choices(
    client, external_module_choice_factory
):
    external_module_choice_factory.create_batch(size=3, username="hpotter", year="2324")
    res = client.get(
        "me/2324/external-modules/choices",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_student_can_submit_valid_external_module_registration(client):
    module_code = "70007"
    res = client.post(
        "me/2324/external-modules/choices",
        json={"module_code": module_code},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    module = res.json()
    assert module["module_code"] == module_code


def test_student_cant_submit_module_reg_if_external_module_choice_exists(
    client, external_module_choice_factory
):
    module_code = "70007"
    external_module_choice_factory(
        module_code=module_code, username="hpotter", year="2324"
    )
    res = client.post(
        "me/2324/external-modules/choices",
        json={"module_code": module_code},
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "You have already applied for this module."
