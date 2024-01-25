import os

from sqlmodel import create_engine

DEV_URL = "postgresql://user:pass@localhost"

FULL_DB_URL: str = os.environ.get("DB_CONN_STR", f"{DEV_URL}/module_subscriptions")
engine = create_engine(FULL_DB_URL)
