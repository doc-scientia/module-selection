import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    environment: str = os.getenv("ENVIRONMENT", "development")
    testing: bool = bool(os.getenv("TESTING", 0))

    api_role_username: str = os.getenv("API_ROLE_USERNAME", "api-role-user")
    api_role_password: str = os.getenv("API_ROLE_PASSWORD", "api-role-password")

    # APIs entrypoints
    abc_entrypoint = "https://abc-api.doc.ic.ac.uk"
