from contextlib import contextmanager
from datetime import datetime, timedelta

import typer
from sqlalchemy import text
from sqlmodel import SQLModel
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


@cli.command(name="erase_data")
def erase_data():
    """
    WARNING: This command will erase all data from the tables without dropping the tables.
    """
    confirm = typer.confirm(
        "Are you sure you want to erase all data from the tables? This action cannot be undone."
    )
    if confirm:
        session = next(get_session())

        # Iterate over all tables and delete data
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.execute(text(f"DELETE FROM {table.name}"))  # nosec
        session.commit()
        typer.echo("All data erased successfully.")
    else:
        typer.echo("Operation cancelled.")


@cli.command(name="populate_db")
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
