from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.dependencies import get_current_user, get_session
from app.schemas.module_choices import ExternalModuleOnOffer

modules_on_offer_router = APIRouter(prefix="/{year}")


@modules_on_offer_router.get(
    "/external-modules/on-offer",
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
