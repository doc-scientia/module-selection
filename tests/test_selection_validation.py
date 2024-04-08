import pytest

from app.schemas.internal_modules import ExamTimetableConstraint
from app.selection_validation import (
    compute_exam_timetable_clash,
    is_within_offering_group_bounds,
)


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


def test_clashing_module_code_returned_on_computation_of_exam_timetable_clash(
    session,
    internal_module_on_offer_factory,
):
    module = internal_module_on_offer_factory(
        exam_timetable_constraint=ExamTimetableConstraint.Tx101,
        with_regulations=[
            dict(
                with_enrollments=[dict(username="hpotter")],
            )
        ],
    )
    assert (
        compute_exam_timetable_clash(
            session, module.year, "hpotter", module.exam_timetable_constraint
        )
        is module.code
    )


def test_none_returned_on_computation_of_exam_timetable_clash_if_no_clashing_module(
    session,
):
    assert (
        compute_exam_timetable_clash(
            session, "2324", "hpotter", ExamTimetableConstraint.Tx101
        )
        is None
    )
