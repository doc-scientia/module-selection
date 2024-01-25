from typing import Any

from starlette import status
from starlette.responses import Response


class UpstreamResponse:
    response: Any
    content: dict | list[dict] | bytes | None = None
    true_status_code: int = -1

    def __init__(self, response, *args, **kwargs):
        self._response = response

    def to_response(self, status_code_override=None) -> Response:
        return Response(
            headers=self._response.headers if self._response else None,
            content=self._response.content,
            status_code=status_code_override or self._response.status_code,
        )

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def is_ok(self) -> bool:
        return self._response.status_code == status.HTTP_200_OK

    @property
    def json_content(self) -> dict:
        return self._response.json()
