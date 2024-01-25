from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from app.doc_upstream_services.response_wrappers import UpstreamResponse


class DocUpstreamService:
    def __init__(
        self,
        service_entrypoint: str,
        connection_username: str,
        connection_password: str,
    ):
        self.service_entrypoint = service_entrypoint
        self.connection_username = connection_username
        self.connection_password = connection_password

    def make_request(
        self,
        url: str,
        method: str = "get",
        params: Any = None,
        proxied_user: str | None = None,
        data: str | None = None,
        files: list[tuple[str, bytes]] | None = None,
    ) -> UpstreamResponse:
        attributes: dict[str, Any] = dict(
            auth=HTTPBasicAuth(self.connection_username, self.connection_password)
        )
        if proxied_user:
            attributes["headers"] = {"X-PROXIED-USER": proxied_user}
        if params:
            attributes["params"] = params
        if data:
            attributes["data"] = data
        if files:
            attributes["files"] = (
                [("file", files[0])]
                if len(files) == 1
                else [("files", f) for f in files]
            )

        response: requests.Response = getattr(requests, method)(
            f"{self.service_entrypoint}{url}", **attributes
        )
        return UpstreamResponse(response)
