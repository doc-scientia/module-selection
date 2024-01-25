from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from starlette import status
from starlette.responses import Response

from app.dependencies import get_current_user, get_session
from app.request_checks import verify_user_is_tutor_or_uta
from app.schemas.tutoring_sessions import (
    TutoringSession,
    TutoringSessionAttendance,
    TutoringSessionRead,
    TutoringSessionWrite,
)

sessions_router = APIRouter(
    prefix="/{year}/sessions", dependencies=[Depends(verify_user_is_tutor_or_uta)]
)


@sessions_router.get(
    "", tags=["tutoring-sessions"], response_model=list[TutoringSessionRead]
)
def get_sessions(
    year: str,
    groups: list[str] = Query([], alias="group"),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(TutoringSession).where(TutoringSession.year == year)
    query = query.where(TutoringSession.group.in_(groups)) if groups else query  # type: ignore
    query_result = session.exec(query).all()
    return query_result


@sessions_router.post(
    "", tags=["tutoring-sessions"], response_model=TutoringSessionRead
)
def create_session(
    year: str,
    tutoring_session: TutoringSessionWrite,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    attendance_db_items = [
        TutoringSessionAttendance(**a.dict()) for a in tutoring_session.attendances
    ]
    tutoring_session_dict = tutoring_session.dict()
    tutoring_session_dict.update(attendances=attendance_db_items, year=year)
    tutoring_session_db_item = TutoringSession(**tutoring_session_dict)
    session.add(tutoring_session_db_item)
    session.commit()
    return tutoring_session_db_item


@sessions_router.put(
    "/{session_id}", tags=["tutoring-sessions"], response_model=TutoringSessionRead
)
def update_session(
    year: str,
    session_id: int,
    new_tutoring_session: TutoringSessionWrite,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    existing_session = session.get(TutoringSession, session_id)
    if existing_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tutoring session not found.",
        )
    new_tutoring_session_dict = new_tutoring_session.dict()
    attendances_dict = new_tutoring_session_dict.pop("attendances")
    attendance_db_items = [TutoringSessionAttendance(**a) for a in attendances_dict]
    for k, v in new_tutoring_session_dict.items():
        setattr(existing_session, k, v)
    existing_session.attendances = attendance_db_items
    session.add(existing_session)
    session.commit()
    return existing_session


@sessions_router.delete(
    "/{session_id}", tags=["tutoring-sessions"], response_model=TutoringSessionRead
)
def delete_session(
    year: str,
    session_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    existing_session = session.get(TutoringSession, session_id)
    if existing_session is not None:
        session.delete(existing_session)
        session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
