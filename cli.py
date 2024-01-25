import typer
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import SQLModel

from app.database.connection import engine

cli = typer.Typer()


@cli.command()
def create_tables():
    SQLModel.metadata.create_all(engine)


# python cli.py delete-database
@cli.command()
def delete_database():
    if database_exists(engine.url):
        drop_database(engine.url)


# python cli.py create-db
@cli.command()
def create_db():
    print("db exists") if database_exists(engine.url) else create_database(engine.url)


if __name__ == "__main__":
    cli()
