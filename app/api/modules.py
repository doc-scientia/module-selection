import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, delete, select

from app.dependencies import get_session
from app.schemas.modules import Enrolment, Module

module_router = APIRouter(prefix="/{year}")


@module_router.get(
    "/subscribed_modules/{student_username}",
    tags=["modules"],
    response_model=list[str],
)
def subscribed_modules(student_username, session: Session = Depends(get_session)):
    query = select(Module).where(Enrolment.student_username == student_username)
    return [module.module_code for module in session.exec(query).all()]


def is_valid_combination(modules: list[int]):
    ##Needs to be implemented according to logic for determining what is valid and what isn't
    ##currently a placeholder for testing
    return len(modules) > 0


@module_router.post(
    "/subscribed_modules/{student_username}",
    tags=["moduleselection"],
    response_model=list[str],
)
async def submit_subscribed_modules(
    student_username, request: Request, session: Session = Depends(get_session)
):
    data = await request.json()
    module_codes = data["module_codes"]
    if not is_valid_combination(module_codes):
        raise HTTPException(status_code=400, detail="Invalid Module Selection.")

    session.exec(
        delete(Enrolment).where(Enrolment.student_username == student_username)  # type: ignore
    )
    modules_to_subscribe_to = session.exec(
        select(Module).where(Module.module_code.in_(module_codes))  # type: ignore
    ).all()

    new_modules = []
    for module in modules_to_subscribe_to:
        new_enrolment = Enrolment(
            student_username=student_username,
            module=module.id,
            enrolment_date=datetime.datetime.now(),
            enrolment_type="Test Enrolment",
        )
        session.add(new_enrolment)
        new_modules.append(module.module_code)

    session.commit()

    return new_modules


@module_router.get("/all_modules", tags=["all_modules"], response_model=list[Module])
def all_modules(year, session: Session = Depends(get_session)):
    query = select(Module).where(Module.year == year)
    return session.exec(query).all()
