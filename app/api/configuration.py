from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.dependencies import get_current_user, get_session
from app.schemas.configurations import Configuration, ConfigurationRead

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
