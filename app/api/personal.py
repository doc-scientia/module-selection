from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status
from starlette.responses import Response

from app.dependencies import get_current_user, get_session
from app.request_checks import verify_user_is_staff
from app.schemas import PersonalTutoringMeeting
from app.schemas.personal_tutoring_meeting import (
    PersonalTutorMeetingRead,
    PersonalTutorMeetingUpdate,
    PersonalTutorMeetingWrite,
)
from app.schemas.tutoring_sessions import (
    StudentTutoringSessionAttendanceRead,
    TutoringSession,
    TutoringSessionAttendance,
)

personal_router = APIRouter(prefix="/me/{year}")


@personal_router.get(
    "/sessions",
    tags=["personal"],
    response_model=list[StudentTutoringSessionAttendanceRead],
)
def get_personal_sessions(
    year: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = (
        select(TutoringSession, TutoringSessionAttendance)
        .join(TutoringSessionAttendance)
        .where(
            TutoringSession.year == year,
            TutoringSessionAttendance.username == current_user,
        )
    )
    query_result = session.exec(query).all()
    return [
        StudentTutoringSessionAttendanceRead.from_orm(s, update=dict(present=a.present))
        for s, a in query_result
    ]


@personal_router.get(
    "/pt-meetings",
    tags=["personal"],
    response_model=list[PersonalTutorMeetingRead],
)
def get_pt_meetings(
    year: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
    access_control=Depends(verify_user_is_staff),
):
    pt_query = (
        select(PersonalTutoringMeeting)
        .where(PersonalTutoringMeeting.year == year)
        .where(PersonalTutoringMeeting.tutor == current_user)
    )
    return session.exec(pt_query).all()


@personal_router.post(
    "/pt-meetings",
    tags=["personal"],
    response_model=PersonalTutorMeetingRead,
)
def post_pt_meetings(
    year: str,
    pt_meeting: PersonalTutorMeetingWrite,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
    access_control=Depends(verify_user_is_staff),
):
    meeting = PersonalTutoringMeeting(
        **pt_meeting.dict(),
        year=year,
        tutor=current_user,
    )

    session.add(meeting)
    session.commit()
    return meeting


@personal_router.put(
    "/pt-meetings/{meeting_id}",
    tags=["personal"],
    response_model=PersonalTutorMeetingRead,
)
def edit_pt_meetings(
    meeting_id: int,
    update_payload: PersonalTutorMeetingUpdate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
    access_control=Depends(verify_user_is_staff),
):
    meeting = session.get(PersonalTutoringMeeting, meeting_id)
    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal meeting not found.",
        )

    if meeting.tutor != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this meeting",
        )

    for k, v in update_payload.dict().items():
        setattr(meeting, k, v)

    session.commit()
    return meeting


@personal_router.delete("/pt-meetings/{meeting_id}", tags=["personal"])
def delete_pt_meetings(
    meeting_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
    access_control=Depends(verify_user_is_staff),
):
    meeting = session.get(PersonalTutoringMeeting, meeting_id)

    if meeting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal meeting not found.",
        )

    if meeting.tutor != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this meeting",
        )

    session.delete(meeting)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
