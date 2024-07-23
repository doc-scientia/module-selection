import os

from sqlmodel import create_engine

DEV_URL = "postgresql://user:pass@localhost"
FULL_DB_URL: str = os.environ.get("DB_URL", os.environ.get("POSTGRES_URL", f"{DEV_URL}/module_subscriptions")).replace("postgres://", "postgresql://")

def get_db_string() -> str:

	if os.environ.get("AZURE_POSTGRESQL_HOST") is None:
		return FULL_DB_URL

	hostname = os.environ.get("AZURE_POSTGRESQL_HOST")
	port = os.environ.get("AZURE_POSTGRESQL_PORT")
	database = os.environ.get("AZURE_POSTGRESQL_DATABASE")
	username = os.environ.get("AZURE_POSTGRESQL_USERNAME")
	password = os.environ.get("AZURE_POSTGRESQL_PASSWORD")

	return f"postgresql://{username}:{password}@{hostname}:{port}/{database}"

engine = create_engine(get_db_string())





