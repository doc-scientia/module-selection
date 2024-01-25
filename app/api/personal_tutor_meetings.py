from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.dependencies import get_current_user, get_session
from app.request_checks import verify_user_is_staff
from app.schemas import PersonalTutoringMeeting
from app.schemas.personal_tutoring_meeting import PersonalTutorMeetingRead

pt_meetings_router = APIRouter(
    prefix="/{year}/pt-meetings", dependencies=[Depends(verify_user_is_staff)]
)


@pt_meetings_router.get(
    "",
    tags=["personal tutor meetings"],
    response_model=list[PersonalTutorMeetingRead],
)
def get_pt_meetings(
    year: str,
    tutors: list[str] = Query([], alias="tutor"),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(PersonalTutoringMeeting).where(PersonalTutoringMeeting.year == year)
    query = query.where(PersonalTutoringMeeting.tutor.in_(tutors)) if tutors else query  # type: ignore
    return session.exec(query).all()
