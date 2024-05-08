from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.dependencies.main import get_abc_service_handler, get_current_user, get_session
from app.dependencies.preconditions import verify_module_selection_is_open
from app.protocols import AbcUpstreamService
from app.schemas.external_modules import (
    ExternalModuleChoice,
    ExternalModuleChoiceRead,
    ExternalModuleChoiceWrite,
    ExternalModuleOnOffer,
)
from app.schemas.internal_modules import (
    DegreeRegulations,
    InternalModuleChoice,
    InternalModuleChoiceRead,
    InternalModuleChoiceWrite,
    InternalModuleOnOffer,
)
from app.selection_validation import (
    compute_exam_timetable_clash,
    is_within_max_ects_for_degree,
    is_within_offering_group_bounds,
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
    _: str = Depends(verify_module_selection_is_open),
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


@personal_router.delete(
    "/internal-modules/choices/{choice_id}",
    status_code=204,
    tags=["personal module choices"],
)
async def delete_personal_internal_module_choice(
    year: str,
    choice_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
    _: str = Depends(verify_module_selection_is_open),
):
    query = (
        select(InternalModuleChoice)
        .join(DegreeRegulations)
        .join(InternalModuleOnOffer)
        .where(
            InternalModuleOnOffer.year == year,
            InternalModuleChoice.id == choice_id,
        )
    )

    enrolment = session.exec(query).first()
    if not enrolment:
        raise HTTPException(
            status_code=404,
            detail="No internal module choice exists for this module id",
        )

    if enrolment.username != current_user:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this module choice as it belongs to another user.",
        )

    session.delete(enrolment)
    session.commit()


@personal_router.get(
    "/internal-modules/choices",
    response_model=list[InternalModuleChoiceRead],
    tags=["personal module choices"],
)
async def get_personal_internal_module_choices(
    year: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    username = current_user
    query = (
        select(InternalModuleChoice)
        .join(DegreeRegulations)
        .join(InternalModuleOnOffer)
        .where(
            InternalModuleOnOffer.year == year,
            InternalModuleChoice.username == username,
        )
    )
    return session.exec(query).all()


@personal_router.post(
    "/internal-modules/choices",
    response_model=InternalModuleChoiceRead,
    tags=["personal module choices"],
)
async def apply_for_internal_module(
    year: str,
    selection: InternalModuleChoiceWrite,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
    abc_api: AbcUpstreamService = Depends(get_abc_service_handler),
    _: str = Depends(verify_module_selection_is_open),
):
    student = abc_api.get_student(year, current_user)
    query = select(InternalModuleOnOffer).where(
        InternalModuleOnOffer.year == year,
        InternalModuleOnOffer.code == selection.module_code,
    )
    module = session.exec(query).first()
    if not module:
        raise HTTPException(
            status_code=404,
            detail=f"Module with code '{selection.module_code}' not found.",
        )
    regulations = next(
        (r for r in module.regulations if r.degree == student.degree_year), None
    )
    if not regulations:
        raise HTTPException(
            status_code=400,
            detail=f"Module with code '{selection.module_code}' not offered to degree '{student.degree_year}'.",
        )

    if next((e for e in regulations.enrollments if e.username == current_user), None):
        raise HTTPException(
            status_code=400, detail="You have already applied for this module."
        )

    if not is_within_max_ects_for_degree(
        session, year, regulations.degree, current_user, regulations.ects
    ):
        raise HTTPException(
            status_code=400,
            detail="You can't select this module as doing so would violate the total ECTS allowance for the degree.",
        )

    if not is_within_offering_group_bounds(
        session, current_user, regulations.offering_group, regulations.ects
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Your selection violates the maximum number of ects for {regulations.offering_group.label}.",
        )

    if clash := compute_exam_timetable_clash(
        session, year, current_user, regulations.module.exam_timetable_constraint
    ):
        raise HTTPException(
            status_code=400,
            detail=f"The chosen module timetable clashes with the following selected module: {clash}.",
        )

    new_enrollment = InternalModuleChoice(
        username=current_user, degree_regulations=regulations
    )
    session.add(new_enrollment)
    session.commit()
    session.refresh(new_enrollment)
    return new_enrollment
