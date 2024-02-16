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
