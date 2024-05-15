from fastapi import APIRouter, Depends, Path, Query
from sqlmodel import Session, select

from app.dependencies.main import get_current_user, get_session
from app.schemas.external_modules import ExternalModuleOnOffer
from app.schemas.internal_modules import (
    InternalModuleOnOffer,
    InternalModuleOnOfferRead,
)

modules_on_offer_router = APIRouter(prefix="/{year}/on-offer")


@modules_on_offer_router.get(
    "/external-modules",
    tags=["on offer"],
    response_model=list[ExternalModuleOnOffer],
    summary="Get External Modules On Offer",
    description="""
Retrieves a list of external modules that are currently on offer for a specified academic year. This allows users to view the range of available external courses.

**Access**: Accessible to all current students and staff.

**Usage**:
- The `year` parameter specifies the academic year for which the external modules on offer are being queried.
"""
)
def get_external_modules_on_offer(
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(ExternalModuleOnOffer)
    all_external_modules_on_offer = session.exec(query).all()
    return all_external_modules_on_offer


@modules_on_offer_router.get(
    "/internal-modules",
    tags=["on offer"],
    response_model=list[InternalModuleOnOfferRead],
    summary="Get Internal Modules On Offer",
    description="""
Retrieves a list of internal modules currently on offer for the specified academic year, optionally filtered by degrees. This is useful for users looking to understand the internal academic offerings available.

**Access**: Accessible to all students and staff.

**Usage**:
- The `year` parameter specifies the academic year for which internal modules on offer are queried.
- The optional `degrees` query parameter can be used to filter the results by specific degrees, enhancing search specificity.
"""
)
def get_internal_modules_on_offer(
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    degrees: list[str]
    | None = Query(None, alias="degree", description="Degree filter"),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(InternalModuleOnOffer).where(InternalModuleOnOffer.year == year)
    all_internal_modules_on_offer = session.exec(query).all()
    if degrees:
        relevant_modules = []
        for m in all_internal_modules_on_offer:
            if updated_regs := [r for r in m.regulations if r.degree in degrees]:
                m.regulations = updated_regs
                relevant_modules.append(m)
        return relevant_modules
    return all_internal_modules_on_offer
