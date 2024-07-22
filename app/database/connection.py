import os

from sqlmodel import create_engine

DEV_URL = "postgresql://user:pass@localhost"
FULL_DB_URL: str = os.environ.get("DB_URL", os.environ.get("POSTGRES_URL", f"{DEV_URL}/module_subscriptions")).replace("postgres://", "postgresql://")

engine = create_engine(FULL_DB_URL)
