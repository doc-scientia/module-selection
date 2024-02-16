from tests.conftest import HPOTTER_CREDENTIALS


def test_student_can_get_subscribed_modules(client, configuration_factory):
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
