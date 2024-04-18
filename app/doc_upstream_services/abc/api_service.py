from app.doc_upstream_services.abc.deserialisation import deserialize_or_502
from app.doc_upstream_services.abc.schemas import Student
from app.doc_upstream_services.base_service import DocUpstreamService
from app.doc_upstream_services.response_wrappers import UpstreamResponse
from app.protocols import AbcUpstreamService


class AbcAPIService(DocUpstreamService, AbcUpstreamService):
    def get_staff(
        self,
        year: str,
        login: str,
        proxied_user: str | None = None,
    ) -> UpstreamResponse:
        return self.make_request(
            f"/{year}/staff?login={login}",
            proxied_user=proxied_user,
        )

    def get_student(
        self,
        year: str,
        login: str,
        proxied_user: str | None = None,
    ) -> Student:
        res = self.make_request(
            f"/{year}/students/{login}",
            proxied_user=proxied_user,
        )
        return deserialize_or_502(res, Student)
