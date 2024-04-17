from fastapi import Depends
from sqlalchemy import exists
from sqlmodel import Session

from app.dependencies.main import get_current_user, get_session
from app.schemas.admin import Admin


def verify_user_is_admin(
        username=Depends(get_current_user), session: Session = Depends(get_session)
):
    return session.query(exists().where(Admin.username == username)).scalar()
