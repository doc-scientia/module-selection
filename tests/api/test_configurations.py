from datetime import datetime

from app.utils.datetime import to_datetime_string
from tests.conftest import HPOTTER_CREDENTIALS


def test_can_get_module_selection_configuration_by_degree_year(
    client, configuration_factory
):
    configuration = configuration_factory(with_periods=1)
    res = client.get(
        f"/{configuration.year}/configurations/{configuration.degree_year}",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    response = res.json()
    assert response["degree_year"] == configuration.degree_year
    assert response["status"] == configuration.status
    assert len(response["periods"]) == 1


def test_can_get_module_selection_configurations(client, configuration_factory):
    configuration_factory.create_batch(size=2, year="2324")
    res = client.get(
        "/2324/configurations",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_non_year_coordinator_patching_a_configuration_gets_403(
    client, configuration_factory
):
    pass


def test_year_coordinator_can_patch_a_module_selection_configuration_status(
    client, configuration_factory
):
    configuration = configuration_factory()
    payload = {"status": "open"}
    res = client.patch(
        f"/{configuration.year}/configurations/{configuration.id}",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    assert res.json()["status"] == payload["status"]


def test_year_coordinator_can_post_a_new_module_selection_period(
    client, configuration_factory
):
    configuration = configuration_factory()
    payload = {
        "start": to_datetime_string(datetime(2024, 3, 1, 14)),
        "end": to_datetime_string(datetime(2024, 3, 15, 19)),
    }
    res = client.post(
        f"/{configuration.year}/configurations/{configuration.id}/periods",
        json=payload,
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    response = res.json()
    assert response["start"] == payload["start"]
    assert response["end"] == payload["end"]
