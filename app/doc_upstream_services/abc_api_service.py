from app.doc_upstream_services.base_service import DocUpstreamService
from app.doc_upstream_services.response_wrappers import UpstreamResponse
from app.protocols import AbcUpstreamService


class AbcAPIService(DocUpstreamService, AbcUpstreamService):
    def get_staff_info(
        self,
        year: str,
        login: str,
        proxied_user: str | None = None,
    ) -> UpstreamResponse:
        return self.make_request(
            f"/{year}/staff-optimised?login={login}",
            proxied_user=proxied_user,
        )

    def get_student_info(
        self,
        year: str,
        login: str,
        proxied_user: str | None = None,
    ) -> UpstreamResponse:
        return self.make_request(
            f"/{year}/students-optimised?login={login}",
            proxied_user=proxied_user,
        )

    def get_tutorial_groups(
        self,
        year: str,
        module_codes: list[str] | None = None,
        numbers: list[int] | None = None,
        types: list[str] | None = None,
        proxied_user: str | None = None,
    ) -> UpstreamResponse:
        params = {"number": numbers, "module_code": module_codes, "type": types}
        params = {k: v for k, v in params.items() if v is not None}
        return self.make_request(
            f"/{year}/tutorial-groups",
            params=params,
            proxied_user=proxied_user,
        )
