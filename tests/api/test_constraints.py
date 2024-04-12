from tests.conftest import HPOTTER_CREDENTIALS


def test_getting_constraints_for_non_existing_degree_gives_404(client):
    res = client.get(
        "/2324/constraints/xyz",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Degree xyz not found in 2324."


def test_constraint_for_existing_degree_is_well_formed(
    client, internal_module_on_offer_factory, degree_ects_constraints_factory
):
    dcs = degree_ects_constraints_factory()
    internal_module_on_offer_factory.create_batch(
        size=3, year=dcs.year, with_regulations=[dict(year=dcs.year, degree=dcs.degree)]
    )
    res = client.get(
        f"/{dcs.year}/constraints/{dcs.degree}",
        auth=HPOTTER_CREDENTIALS,
    )
    assert res.status_code == 200
    assert res.json()["year"] == dcs.year
    assert res.json()["degree"] == dcs.degree
    assert res.json()["degree_constraints"]["min"] == dcs.min
    assert res.json()["degree_constraints"]["max"] == dcs.max
    assert len(res.json()["offering_group_constraints"]) == 3
