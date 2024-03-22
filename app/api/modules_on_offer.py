from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.dependencies.main import get_current_user, get_session
from app.schemas.external_modules import ExternalModuleOnOffer
from app.schemas.internal_modules import (
    CohortRegulations,
    InternalModuleOnOffer,
    InternalModuleOnOfferRead,
)

modules_on_offer_router = APIRouter(prefix="/{year}/on-offer")


@modules_on_offer_router.get(
    "/external-modules",
    tags=["on offer"],
    response_model=list[ExternalModuleOnOffer],
)
def get_external_modules_on_offer(
    year: str,
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
)
def get_internal_modules_on_offer(
    year: str,
    cohorts: list[str]
    | None = Query(None, alias="cohort", description="Cohort filter"),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = (
        select(InternalModuleOnOffer)
        .join(CohortRegulations)
        .where(InternalModuleOnOffer.year == year)
    )
    query = query.where(CohortRegulations.cohort.in_(cohorts)) if cohorts else query  # type: ignore
    all_internal_modules_on_offer = session.exec(query).all()
    return all_internal_modules_on_offer
