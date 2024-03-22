from tests.conftest import HPOTTER_CREDENTIALS


def test_user_can_get_external_modules_on_offer(
    client, external_module_on_offer_factory
):
    external_module_on_offer_factory.create_batch(size=3, year="2324")
    res = client.get("/2324/on-offer/external-modules", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 3
