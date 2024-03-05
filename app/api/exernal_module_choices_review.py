from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from app.dependencies import get_current_user, get_session
from app.schemas.module_choices import (
    ExternalModuleChoice,
    ExternalModuleChoiceRead,
    ExternalModuleChoiceUpdate,
)

external_module_choices_review_router = APIRouter(
    prefix="/{year}/external-module-choices",
    tags=["choices"],
    # dependencies=[Depends(verify_user_is_enrolments_admin)]  TODO: determine right role and implement this check
)


@external_module_choices_review_router.get(
    "",
    response_model=list[ExternalModuleChoiceRead],
)
def get_external_module_choices(
    year: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(ExternalModuleChoice).where(ExternalModuleChoice.year == year)

    return session.exec(query).all()


@external_module_choices_review_router.patch(
    "/{choice_id}",
    response_model=ExternalModuleChoiceRead,
)
def update_external_module_choice(
    year: str,
    choice_id: int,
    patch: ExternalModuleChoiceUpdate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(ExternalModuleChoice).where(
        ExternalModuleChoice.year == year, ExternalModuleChoice.id == choice_id
    )
    choice = session.exec(query).first()
    if not choice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External module choice not found.",
        )

    choice.status = patch.status
    choice.reviewed_by = current_user
    choice.reviewed_on = datetime.utcnow()
    session.commit()
    session.refresh(choice)
    return choice