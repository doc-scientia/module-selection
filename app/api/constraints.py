from fastapi import APIRouter, Depends, HTTPException, Path
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
    summary="Get Degree Constraints",
    description="""
Retrieves the constraints associated with a specific degree for a given academic year. This includes ECTS constraints, relevant offering groups constraints (e.g. how many OPTIONAL modules are allowed for the selection, how many SELECTIVE one etc.), and other regulations applicable to the degree.

**Access**: Accessible by current staff and students.

**Usage**:
- The `degree` parameter in the URL path specifies the degree for which constraints are sought, e.g., 'mcai5'.
- The `year` parameter specifies the academic year for which the information is relevant, and should be provided in a short form, e.g., '2324'.

**Raises**: 404 error if constraints for the specified degree and year are not found.
"""
)
def get_degree_constraints(
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    degree: str = Path(..., description="Degree year e.g. mcai5"),
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
