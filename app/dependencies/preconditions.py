from datetime import datetime

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.dependencies.main import get_session
from app.schemas import Configuration, SelectionPeriod
from app.schemas.configurations import ModuleSelectionStatus


def verify_module_selection_is_open(year: str, session: Session = Depends(get_session)):
    now = datetime.utcnow()
    subquery = (
        select(Configuration.id)
        .join(SelectionPeriod)
        .where(
            Configuration.year == year,
            Configuration.status == ModuleSelectionStatus.USE_PERIODS,
            SelectionPeriod.start <= now,
            SelectionPeriod.end >= now,
        )
        .exists()
    )
    if not session.query(subquery).scalar():
        raise HTTPException(
            status_code=403,
            detail=f"Module selection for year {year} is not currently open.",
        )
