from tests.conftest import HPOTTER_CREDENTIALS


def test_user_can_get_internal_modules_on_offer(
    client, internal_module_on_offer_factory
):
    internal_module_on_offer_factory.create_batch(
        size=3, year="2324", with_regulations=2
    )
    res = client.get("/2324/on-offer/internal-modules", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 6


def test_user_can_get_internal_modules_on_offer_by_cohort(
    client, internal_module_on_offer_factory
):
    internal_module_on_offer_factory.create_batch(
        size=3, year="2324", with_regulations=[{"cohort": "c3"}, {"cohort": "v5"}]
    )
    res = client.get(
        "/2324/on-offer/internal-modules?cohort=c3", auth=HPOTTER_CREDENTIALS
    )
    assert res.status_code == 200
    assert len(res.json()) == 3
