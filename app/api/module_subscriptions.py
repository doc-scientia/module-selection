import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, delete, select

from app.dependencies import get_current_user, get_session
from app.schemas.enrolments import Enrolment, ModuleSubscription, EnrolmentRead

module_router = APIRouter(prefix="/{year}")


@module_router.get(
    "/subscribed_modules",
    tags=["module subscriptions"],
    response_model=list[str],
)
def subscribed_modules(
        session: Session = Depends(get_session),
        current_user: str = Depends(get_current_user),
):
    query = select(Enrolment).where(Enrolment.student_username == current_user)
    return [enrolment.module_code for enrolment in session.exec(query).all()]


def is_valid_combination(modules: list[str]):
    # Needs to be implemented according to logic for determining what is valid and what isn't
    # currently a placeholder for testing
    return len(modules) > 0


@module_router.post(
    "/subscribed_modules",
    tags=["module subscriptions"],
    response_model=list[EnrolmentRead],
)
async def submit_subscribed_modules(
        subscriptions: list[ModuleSubscription],
        session: Session = Depends(get_session),
        current_user: str = Depends(get_current_user),
):
    module_codes = [subscription.module_code for subscription in subscriptions]
    if not is_valid_combination(module_codes):
        raise HTTPException(status_code=400, detail="Invalid Module Selection.")

    session.exec(
        delete(Enrolment).where(Enrolment.student_username == current_user)  # type: ignore
    )

    new_enrolments = []
    for module_code in module_codes:
        new_enrolment = Enrolment(
            student_username=current_user,
            module_code=module_code,
            enrolment_date=datetime.datetime.now(),
            enrolment_type="Test Enrolment",
            year='2324'
        )
        session.add(new_enrolment)
        new_enrolments.append(new_enrolment)

    session.commit()

    return new_enrolments
