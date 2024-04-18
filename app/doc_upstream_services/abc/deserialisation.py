from typing import Literal, TypeVar, overload

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

from app.doc_upstream_services.response_wrappers import UpstreamResponse

S = TypeVar("S", bound=BaseModel)


@overload
def deserialize_or_502(
    response: UpstreamResponse, schema_class: type[S], many: Literal[True]
) -> list[S]:
    ...


@overload
def deserialize_or_502(
    response: UpstreamResponse, schema_class: type[S], many: Literal[False]
) -> S:
    ...


@overload
def deserialize_or_502(response: UpstreamResponse, schema_class: type[S]) -> S:
    ...


def deserialize_or_502(
    response: UpstreamResponse, schema_class: type[S], many: bool = False
) -> S | list[S]:
    if response.is_ok:
        json_content = response.json_content
        return (
            [schema_class(**item) for item in json_content]
            if many
            else schema_class(**json_content)
        )
    abc_error_message = response.json_content.get(
        "detail", "no further details available."
    )
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=f"ABC API call returned a {response.status_code}: {abc_error_message}.",
    )
