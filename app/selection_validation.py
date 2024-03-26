from sqlalchemy import func
from sqlmodel import Session, select

from app.schemas import CohortRegulations, InternalModuleChoice, OfferingGroup


def is_within_offering_group_bounds(
    session: Session, student: str, offering_group: OfferingGroup, new_ects: int
) -> bool:
    query = (
        select(
            (
                (func.sum(CohortRegulations.ects) + new_ects >= OfferingGroup.min)
                & (func.sum(CohortRegulations.ects) + new_ects <= OfferingGroup.max)
            ).label("is_within_bounds")
        )
        .join(CohortRegulations)
        .join(InternalModuleChoice)
        .where(
            OfferingGroup.id == offering_group.id,
            InternalModuleChoice.username == student,
        )
        .group_by(OfferingGroup.min, OfferingGroup.max)
    )
    result = session.exec(query).first()
    return True if result is None else result
