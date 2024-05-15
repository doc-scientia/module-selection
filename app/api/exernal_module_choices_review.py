from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select
from starlette import status

from app.dependencies.main import get_current_user, get_session
from app.schemas.external_modules import (
    ExternalModuleChoice,
    ExternalModuleChoiceRead,
    ExternalModuleChoiceUpdate,
    ExternalModuleOnOffer,
)

external_module_choices_review_router = APIRouter(
    prefix="/{year}/external-module-choices",
    tags=["external module choices review"],
    # dependencies=[Depends(verify_user_is_enrolments_admin)]  TODO: determine right role and implement this check
)


@external_module_choices_review_router.get(
    "",
    response_model=list[ExternalModuleChoiceRead],
    summary="Get All External Module Choices",
    description="""
Retrieves all external module choices available for a given academic year. This is used by staff with specific review roles to oversee module selection processes.

**Access**: Accessible only to staff members with the appropriate review role for module selections.

**Usage**:
- The `year` parameter specifies the academic year for which external module choices are being queried.
"""
)
def get_external_module_choices(
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = (
        select(ExternalModuleChoice)
        .join(ExternalModuleOnOffer)
        .where(ExternalModuleOnOffer.year == year)
    )
    return session.exec(query).all()


@external_module_choices_review_router.patch(
    "/{choice_id}",
    response_model=ExternalModuleChoiceRead,
    summary="Update External Module Choice",
    description="""
Allows a staff member with the appropriate review role to update the status of an external module choice for a specified academic year.

**Access**: Accessible only to staff members with the appropriate review role for module selections.

**Usage**:
- The `choice_id` in the URL path identifies the specific external module choice to be updated.
- The `year` parameter in the URL path specifies the academic year associated with the module choice.

**Raises**: 404 error if the specified external module choice is not found.
"""
)
def update_external_module_choice(
    patch: ExternalModuleChoiceUpdate,
    year: str = Path(..., description="Academic year in short form e.g. 2324"),
    choice_id: int = Path(..., description="Choice id"),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = (
        select(ExternalModuleChoice)
        .join(ExternalModuleOnOffer)
        .where(ExternalModuleOnOffer.year == year, ExternalModuleChoice.id == choice_id)
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