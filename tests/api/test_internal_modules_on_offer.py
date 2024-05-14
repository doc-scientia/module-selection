from tests.conftest import HPOTTER_CREDENTIALS


def test_user_can_get_internal_modules_on_offer(
    client, internal_module_on_offer_factory
):
    internal_module_on_offer_factory.create_batch(
        size=3, year="2324", with_regulations=2
    )
    res = client.get("/2324/on-offer/internal-modules", auth=HPOTTER_CREDENTIALS)
    assert res.status_code == 200
    assert len(res.json()) == 3
    assert all(len(module["regulations"]) == 2 for module in res.json())


def test_user_can_get_internal_modules_on_offer_by_cohort(
    client, internal_module_on_offer_factory
):
    internal_module_on_offer_factory.create_batch(
        size=3,
        year="2324",
        with_regulations=[
            {"degree": "mc", "degree_year": 3},
            {"degree": "bc", "degree_year": 3},
        ],
    )
    res = client.get(
        "/2324/on-offer/internal-modules?degree=mc", auth=HPOTTER_CREDENTIALS
    )
    assert res.status_code == 200
    assert len(res.json()) == 3
    assert all(len(module["regulations"]) == 1 for module in res.json())
