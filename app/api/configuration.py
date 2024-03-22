from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status
from starlette.responses import Response

from app.dependencies.main import get_current_user, get_session
from app.schemas.configurations import (
    Configuration,
    ConfigurationRead,
    ConfigurationWrite,
    SelectionPeriod,
    SelectionPeriodRead,
    SelectionPeriodWrite,
)

module_selection_configuration = APIRouter(
    prefix="/{year}/configuration", tags=["configuration"]
)


@module_selection_configuration.get(
    "",
    response_model=ConfigurationRead,
)
def get_module_selection_configuration(
    year: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(Configuration).where(Configuration.year == year)

    configuration = session.exec(query).first()
    if not configuration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection configuration not found.",
        )
    return configuration


@module_selection_configuration.patch(
    "",
    response_model=ConfigurationRead,
)
def update_module_selection_configuration(
    year: str,
    patch: ConfigurationWrite,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(Configuration).where(Configuration.year == year)
    configuration = session.exec(query).first()
    if not configuration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection configuration not found.",
        )
    patch_data = patch.dict(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(configuration, key, value)
    session.commit()
    session.refresh(configuration)
    return configuration


@module_selection_configuration.post(
    "/periods",
    response_model=SelectionPeriodRead,
)
def add_new_module_selection_period(
    year: str,
    payload: SelectionPeriodWrite,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(Configuration).where(Configuration.year == year)
    configuration = session.exec(query).first()
    if not configuration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection configuration not found.",
        )
    new_period = SelectionPeriod(**payload.dict(), configuration=configuration)
    session.add(new_period)
    session.commit()
    return new_period


@module_selection_configuration.delete(
    "/periods/{period_id}", status_code=204, response_class=Response
)
def delete_module_selection_period(
    year: str,
    period_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = (
        select(SelectionPeriod)
        .join(Configuration)
        .where(
            SelectionPeriod.id == period_id,
            Configuration.year == year,
        )
    )
    period = session.exec(query).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection period not found.",
        )
    session.delete(period)
    session.commit()


@module_selection_configuration.put(
    "/periods/{period_id}", response_model=SelectionPeriodRead
)
def update_module_selection_period(
    year: str,
    period_id: int,
    payload: SelectionPeriodWrite,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = (
        select(SelectionPeriod)
        .join(Configuration)
        .where(
            SelectionPeriod.id == period_id,
            Configuration.year == year,
        )
    )
    period = session.exec(query).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module selection period not found.",
        )
    for key, value in payload.dict().items():
        setattr(period, key, value)
    session.commit()
    session.refresh(period)
    return period
