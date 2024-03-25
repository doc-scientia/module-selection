from contextlib import contextmanager
from datetime import datetime, timedelta

import typer
from typer import Argument

from app.dependencies.main import get_session
from app.factories import (
    ConfigurationFactory,
    ExternalModuleOnOfferFactory,
    InternalModuleOnOfferFactory,
    all_factories,
)
from app.schemas.configurations import ModuleSelectionStatus
from app.schemas.internal_modules import OfferingGroup

cli = typer.Typer()


@contextmanager
def dynamic_session():
    session = next(get_session())
    for f in all_factories:
        f._meta.sqlalchemy_session = session
    yield


@cli.command()
def populate_db(
    year: str = Argument(help="Academic year in short form e.g. 2324 for 2023-2024"),
):
    """
    Populates the database with dummy data.
    """
    with dynamic_session():
        ConfigurationFactory(
            year=year,
            with_periods=[dict(end=datetime.utcnow() + timedelta(weeks=2))],
            status=ModuleSelectionStatus.USE_PERIODS,
        )
        ExternalModuleOnOfferFactory.create_batch(size=3, year=year)
        InternalModuleOnOfferFactory.create_batch(
            size=5,
            year=year,
            with_regulations=[
                dict(cohort="c3", offering_group=OfferingGroup.OPTIONAL),
                dict(cohort="v5", offering_group=OfferingGroup.SELECTIVE),
            ],
        )
        InternalModuleOnOfferFactory.create_batch(
            size=3,
            year=year,
            with_regulations=[
                dict(cohort="c3", offering_group=OfferingGroup.SELECTIVE),
            ],
        )
    print("Database populated successfully.")


if __name__ == "__main__":
    cli()
