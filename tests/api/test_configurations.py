from datetime import datetime

from app.utils.datetime import to_datetime_string
from tests.conftest import HPOTTER_CREDENTIALS


def test_can_get_module_selection_configuration(client, configuration_factory):
    configuration = configuration_factory(with_periods=1)
    res = client.get(
        f"/{configuration.year}/configuration",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    response = res.json()
    assert response["status"] == configuration.status
    assert len(response["periods"]) == 1


def test_getting_a_non_existing_module_selection_configuration_by_degree_year_gives_404(
    client,
):
    res = client.get(
        "/1234/configuration",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module selection configuration not found."


def test_non_year_coordinator_patching_a_configuration_gets_403(
    client, configuration_factory
):
    pass


def test_year_coordinator_can_patch_a_module_selection_configuration_status(
    client, configuration_factory
):
    configuration = configuration_factory()
    payload = {"status": "use_periods"}
    res = client.patch(
        f"/{configuration.year}/configuration",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    assert res.json()["status"] == payload["status"]


def test_patch_a_non_existing_module_selection_configuration_gives_404(client):
    payload = {"status": "use_periods"}
    res = client.patch(
        "/1234/configuration",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module selection configuration not found."


def test_patch_a_module_selection_configuration_for_the_wrong_year_gives_404(
    client, configuration_factory
):
    configuration = configuration_factory()
    payload = {"status": "use_periods"}
    res = client.patch(
        f"/1234/configuration",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module selection configuration not found."


def test_posting_a_new_module_selection_period_against_non_existing_configuration_gives_404(
    client,
):
    payload = {
        "start": to_datetime_string(datetime(2024, 3, 1, 14)),
        "end": to_datetime_string(datetime(2024, 3, 15, 19)),
    }
    res = client.post(
        "/1234/configuration/periods",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module selection configuration not found."


def test_posting_a_new_module_selection_period_against_wrong_year_gives_404(
    client, configuration_factory
):
    configuration = configuration_factory()
    payload = {
        "start": to_datetime_string(datetime(2024, 3, 1, 14)),
        "end": to_datetime_string(datetime(2024, 3, 15, 19)),
    }
    res = client.post(
        f"/1234/configuration/periods",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module selection configuration not found."


def test_year_coordinator_can_post_a_new_module_selection_period(
    client, configuration_factory
):
    configuration = configuration_factory()
    payload = {
        "start": to_datetime_string(datetime(2024, 3, 1, 14)),
        "end": to_datetime_string(datetime(2024, 3, 15, 19)),
    }
    res = client.post(
        f"/{configuration.year}/configuration/periods",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    response = res.json()
    assert response["start"] == payload["start"]
    assert response["end"] == payload["end"]


def test_year_coordinator_can_delete_an_existing_module_selection_period(
    client, configuration_factory
):
    configuration = configuration_factory(with_periods=1)
    [period] = configuration.periods
    res = client.delete(
        f"/{configuration.year}/configuration/periods/{period.id}",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 204
    assert res.content == b""
    assert len(configuration.periods) == 0


def test_deleting_a_module_selection_period_for_a_non_existing_configuration_gives_404(
    client,
):
    res = client.delete(
        "/1234/configuration/periods/1",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module selection period not found."


def test_deleting_a_module_selection_period_for_the_wrong_year_gives_404(
    client, configuration_factory
):
    configuration = configuration_factory(with_periods=1)
    [period] = configuration.periods
    res = client.delete(
        f"/1234/configuration/periods/{period.id}",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module selection period not found."


def test_year_coordinator_can_update_an_existing_module_selection_period(
    client, configuration_factory
):
    payload = {
        "start": to_datetime_string(datetime(2024, 3, 1, 14)),
        "end": to_datetime_string(datetime(2024, 3, 15, 19)),
    }
    configuration = configuration_factory(with_periods=1)
    [period] = configuration.periods
    res = client.put(
        f"/{configuration.year}/configuration/periods/{period.id}",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    assert res.json()["start"] == payload["start"]
    assert res.json()["end"] == payload["end"]


def test_updating_a_module_selection_period_for_a_non_existing_configuration_gives_404(
    client,
):
    payload = {
        "start": to_datetime_string(datetime(2024, 3, 1, 14)),
        "end": to_datetime_string(datetime(2024, 3, 15, 19)),
    }
    res = client.put(
        "/1234/configuration/periods/1",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module selection period not found."


def test_updating_a_module_selection_period_for_the_wrong_year_gives_404(
    client, configuration_factory
):
    payload = {
        "start": to_datetime_string(datetime(2024, 3, 1, 14)),
        "end": to_datetime_string(datetime(2024, 3, 15, 19)),
    }
    configuration = configuration_factory(with_periods=1)
    [period] = configuration.periods
    res = client.put(
        f"/1234/configuration/periods/{period.id}",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Module selection period not found."
