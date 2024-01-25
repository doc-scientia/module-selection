from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.dependencies import get_current_user, get_session
from app.request_checks import verify_user_matches_student_username_or_is_staff_or_tutor
from app.schemas.tutoring_sessions import (
    StudentTutoringSessionAttendanceRead,
    TutoringSession,
    TutoringSessionAttendance,
)

student_tutoring_sessions_router = APIRouter(
    prefix="/{year}/{student_username}/tutoring-sessions",
    dependencies=[Depends(verify_user_matches_student_username_or_is_staff_or_tutor)],
)


@student_tutoring_sessions_router.get(
    "",
    tags=["tutoring-sessions"],
    response_model=list[StudentTutoringSessionAttendanceRead],
)
def get_student_tutoring_attendances(
    year: str,
    student_username: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = (
        select(TutoringSession, TutoringSessionAttendance)
        .join(TutoringSessionAttendance)
        .where(
            TutoringSession.year == year,
            TutoringSessionAttendance.username == student_username,
        )
    )
    query_result = session.exec(query).all()

    return [
        StudentTutoringSessionAttendanceRead.from_orm(s, update=dict(present=a.present))
        for s, a in query_result
    ]
