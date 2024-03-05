from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.dependencies import get_current_user, get_session
from app.schemas.module_choices import ExternalModuleChoice, ExternalModuleChoiceWrite

personal_router = APIRouter(prefix="/me/{year}")


@personal_router.get(
    "/external-modules/choices",
    tags=["personal module choices"],
)
async def get_personal_external_module_choices(
    year: str,
    session: Session = Depends(get_session),
    response_model=list[ExternalModuleChoice],
    current_user: str = Depends(get_current_user),
):
    username = current_user
    query = select(ExternalModuleChoice).where(
        ExternalModuleChoice.year == year,
        ExternalModuleChoice.username == username,
    )
    return session.exec(query).all()


@personal_router.post(
    "/external-modules/choices",
    tags=["personal module choices"],
)
async def apply_for_external_module(
    year: str,
    subscription: ExternalModuleChoiceWrite,
    session: Session = Depends(get_session),
    response_model=ExternalModuleChoice,
    current_user: str = Depends(get_current_user),
):
    username = current_user
    module_code = subscription.module_code

    choice_exists_query = (
        select(ExternalModuleChoice).where(
            ExternalModuleChoice.year == year,
            ExternalModuleChoice.module_code == module_code,
            ExternalModuleChoice.username == username,
        )
    ).exists()

    choice_exists_for_student = session.execute(
        session.query(choice_exists_query)
    ).scalar()

    if choice_exists_for_student:
        raise HTTPException(
            status_code=400, detail="You have already applied for this module."
        )

    new_subscription = ExternalModuleChoice(
        username=username, module_code=module_code, year=year
    )
    session.add(new_subscription)
    session.commit()
    session.refresh(new_subscription)
    return new_subscription
