from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.dependencies import get_current_user, get_session
from app.schemas.module_choices import (
    ExternalModuleChoice,
    ExternalModuleChoiceRead,
    ExternalModuleChoiceWrite,
    ExternalModuleOnOffer,
)

personal_router = APIRouter(prefix="/me/{year}")


@personal_router.get(
    "/external-modules/choices",
    response_model=list[ExternalModuleChoiceRead],
    tags=["personal module choices"],
)
async def get_personal_external_module_choices(
    year: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    username = current_user
    query = (
        select(ExternalModuleChoice)
        .join(ExternalModuleOnOffer)
        .where(
            ExternalModuleOnOffer.year == year,
            ExternalModuleChoice.username == username,
        )
    )
    return session.exec(query).all()


@personal_router.post(
    "/external-modules/choices",
    response_model=ExternalModuleChoiceRead,
    tags=["personal module choices"],
)
async def apply_for_external_module(
    year: str,
    subscription: ExternalModuleChoiceWrite,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    username = current_user
    module_code = subscription.module_code

    query = select(ExternalModuleOnOffer).where(
        ExternalModuleOnOffer.year == year,
        ExternalModuleOnOffer.code == module_code,
    )
    external_module_on_offer = session.exec(query).first()

    if not external_module_on_offer:
        raise HTTPException(
            status_code=404,
            detail=f"External module with code '{module_code}' not found.",
        )
    if current_user in {a.username for a in external_module_on_offer.applications}:
        raise HTTPException(
            status_code=400, detail="You have already applied for this module."
        )

    new_subscription = ExternalModuleChoice(
        username=username, external_module=external_module_on_offer
    )
    session.add(new_subscription)
    session.commit()
    session.refresh(new_subscription)
    return new_subscription
