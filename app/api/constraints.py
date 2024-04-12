from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette.status import HTTP_404_NOT_FOUND

from app.dependencies.main import get_current_user, get_session
from app.schemas import DegreeRegulations
from app.schemas.constraints import (
    ConstraintsRead,
    DegreeECTSConstraints,
    DegreeECTSConstraintsRead,
    OfferingGroup,
    OfferingGroupRead,
)

constraints_router = APIRouter(prefix="/{year}/constraints", tags=["constraints"])


@constraints_router.get(
    "/{degree}",
    response_model=ConstraintsRead,
)
def get_degree_constraints(
    year: str,
    degree: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    degree_constraints_query = select(DegreeECTSConstraints).where(
        DegreeECTSConstraints.year == year, DegreeECTSConstraints.degree == degree
    )
    if degree_constraints := session.exec(degree_constraints_query).first():
        offering_groups_query = (
            select(OfferingGroup)
            .join(DegreeRegulations)
            .where(OfferingGroup.year == year, DegreeRegulations.degree == degree)
            .distinct(OfferingGroup.id)  # type: ignore
        )
        offering_groups = session.exec(offering_groups_query).all()
        return ConstraintsRead(
            year=year,
            degree=degree,
            offering_group_constraints=[
                OfferingGroupRead.from_orm(og) for og in offering_groups
            ],
            degree_constraints=DegreeECTSConstraintsRead.from_orm(degree_constraints),
        )

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f"Degree {degree} not found in {year}.",
    )
