from typing import Protocol

from app.doc_upstream_services.abc.schemas import Student
from app.doc_upstream_services.response_wrappers import UpstreamResponse


class Authenticator(Protocol):
    def authenticate(self, username: str, password: str) -> dict | None:
        """An authenticator can authenticate"""


class AbcUpstreamService(Protocol):
    """
    The ABC API service is the only API that gets mocked in dev.
    This interface ensures type compatibility between the real and the mock connectors.
    """

    def get_staff(
        self,
        year: str,
        login: str,
        proxied_user: str | None = None,
    ) -> UpstreamResponse:
        """ABC API returns current staff record"""

    def get_student(
        self,
        year: str,
        login: str,
        proxied_user: str | None = None,
    ) -> Student:
        """ABC API returns current student record"""
