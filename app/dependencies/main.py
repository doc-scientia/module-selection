from functools import lru_cache
from typing import Generator

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from starlette import status

from app.database.connection import engine
from app.dev_service_providers.ldap_authentication import DummyLdapAuthenticator
from app.dev_upstream_services.abc_api_service import DummyAbcAPIService
from app.doc_upstream_services.abc.api_service import AbcAPIService
from app.ldap_authentication.authenticator import DocLdapAuthenticator
from app.protocols import AbcUpstreamService, Authenticator
from app.settings import Settings

PRIVILEGED_USERS = {
    "adumble",
    "docldap15",
    "ip914",
    "rbc",
    "jsbailey",
    "docldap6",
    "role_user1",
}
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Basic"},
)


SUPERVISOR: str = "SUPERVISOR"
ASSESSOR: str = "ASSESSOR"


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as s:
        try:
            yield s
            s.commit()
        except SQLAlchemyError as e:
            s.rollback()
            raise e


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def get_ldap_handler(settings: Settings = Depends(get_settings)) -> Authenticator:
    if settings.environment == "production":
        return DocLdapAuthenticator()
    return DummyLdapAuthenticator()


basic_auth = HTTPBasic(realm="DoC")


def get_current_user(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
    ldap_handler: Authenticator = Depends(get_ldap_handler),
    x_proxied_user: str = Header(default=None),
) -> str:
    username, password = (
        credentials.username.strip().lower(),
        credentials.password.strip(),
    )
    if ldap_handler.authenticate(username, password) is None:
        raise CREDENTIALS_EXCEPTION

    return (
        x_proxied_user if x_proxied_user and username in PRIVILEGED_USERS else username
    )


def get_abc_service_handler(
    settings: Settings = Depends(get_settings),
) -> AbcUpstreamService:
    if settings.environment == "production":
        return AbcAPIService(
            service_entrypoint=settings.abc_entrypoint,
            connection_username=settings.api_role_username,
            connection_password=settings.api_role_password,
        )
    return DummyAbcAPIService()
