import pytest

from app.selection_validation import is_within_offering_group_bounds


@pytest.mark.parametrize(
    "max_ects, current_ects, new_ects, expected",
    [
        (6, 6, 3, False),
        (6, 6, 1, False),
        (7, 6, 1, True),
        (5, 3, 1, True),
        (5, 3, 2, True),
    ],
)
def test_validation_of_ects_against_offering_group_constraints(
    session,
    offering_group_factory,
    internal_module_on_offer_factory,
    max_ects,
    current_ects,
    new_ects,
    expected,
):
    offering_group = offering_group_factory(min=1, max=max_ects)
    internal_module_on_offer_factory(
        year=offering_group.year,
        with_regulations=[
            dict(
                ects=current_ects,
                offering_group=offering_group,
                with_enrollments=[dict(username="hpotter")],
            )
        ],
    )
    assert (
        is_within_offering_group_bounds(session, "hpotter", offering_group, new_ects)
        is expected
    )
