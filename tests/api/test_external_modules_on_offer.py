from tests.conftest import HPOTTER_CREDENTIALS


def test_year_coordinator_can_get_external_module_choices(
        client, external_module_on_offer_factory
):
    external_module_on_offer_factory.create_batch(size=3, year="2324")
    res = client.get("/2324/external-modules/on-offer", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 3
