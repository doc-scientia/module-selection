from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from app.dependencies import get_current_user, get_session
from app.schemas.configurations import (
    Configuration,
    ConfigurationRead,
    ConfigurationWrite,
)

selection_configurations_router = APIRouter(
    prefix="/{year}/configurations", tags=["configurations"]
)


@selection_configurations_router.get(
    "",
    response_model=list[ConfigurationRead],
)
def get_module_selection_configurations(
    year: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(Configuration).where(Configuration.year == year)
    return session.exec(query).all()


@selection_configurations_router.get(
    "/{degree_year}",
    response_model=ConfigurationRead,
)
def get_module_selection_configuration(
    year: str,
    degree_year: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(Configuration).where(
        Configuration.year == year, Configuration.degree_year == degree_year
    )
    return session.exec(query).first()


@selection_configurations_router.patch(
    "/{configuration_id}",
    response_model=ConfigurationRead,
)
def update_module_selection_configuration(
    year: str,
    configuration_id: int,
    patch: ConfigurationWrite,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    query = select(Configuration).where(Configuration.id == configuration_id)
    configuration = session.exec(query).first()
    if not configuration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    patch_data = patch.dict(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(configuration, key, value)
    session.commit()
    session.refresh(configuration)
    return configuration
