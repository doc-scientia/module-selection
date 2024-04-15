from sqlalchemy import func
from sqlmodel import Session, select

from app.schemas import (
    DegreeECTSConstraints,
    DegreeRegulations,
    InternalModuleChoice,
    InternalModuleOnOffer,
    OfferingGroup,
)
from app.schemas.internal_modules import ExamTimetableConstraint


def is_within_offering_group_bounds(
    session: Session, student: str, offering_group: OfferingGroup, new_ects: float
) -> bool:
    query = (
        select(
            (
                (func.sum(DegreeRegulations.ects) + new_ects >= OfferingGroup.min)
                & (func.sum(DegreeRegulations.ects) + new_ects <= OfferingGroup.max)
            ).label("is_within_bounds")
        )
        .join(DegreeRegulations)
        .join(InternalModuleChoice)
        .where(
            OfferingGroup.id == offering_group.id,
            InternalModuleChoice.username == student,
        )
        .group_by(OfferingGroup.min, OfferingGroup.max)  # type: ignore
    )
    result = session.exec(query).first()
    return True if result is None else result


def compute_exam_timetable_clash(
    session: Session,
    year: str,
    student: str,
    exam_timetable_constraint: ExamTimetableConstraint,
):
    query = (
        select(InternalModuleOnOffer)
        .join(DegreeRegulations)
        .join(InternalModuleChoice)
        .where(
            InternalModuleChoice.username == student,
            InternalModuleOnOffer.year == year,
            InternalModuleOnOffer.exam_timetable_constraint
            == exam_timetable_constraint,
        )
    )
    result = session.exec(query).first()
    return result.code if result else None


def is_within_max_ects_for_degree(
    session: Session,
    year: str,
    degree: str,
    student: str,
    new_ects: float,
):
    # PRE: new_ects value will never alone be more than the maximum ects allowed by the degree
    max_ects_subquery = (
        select(DegreeECTSConstraints.max)
        .where(
            DegreeECTSConstraints.degree == degree,
            DegreeECTSConstraints.year == year,
        )
        .scalar_subquery()
    )

    query = (
        select(func.sum(DegreeRegulations.ects) + new_ects <= max_ects_subquery)
        .select_from(InternalModuleOnOffer)
        .join(DegreeRegulations)
        .join(InternalModuleChoice)
        .where(
            InternalModuleChoice.username == student,
            InternalModuleOnOffer.year == year,
        )
    )
    result = session.exec(query).first()

    return result if result is not None else True
