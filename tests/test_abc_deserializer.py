from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

from app.doc_upstream_services.abc.deserialisation import deserialize_or_502
from app.doc_upstream_services.response_wrappers import UpstreamResponse


class Student(BaseModel):
    name: str
    age: int


# Mocking the response object that will be wrapped by UpstreamResponse
def mock_response(content, status_code=status.HTTP_200_OK):
    mock = Mock()
    mock.status_code = status_code
    mock.json.return_value = content
    return mock


def test_deserialize_or_502_supports_single_deserialization():
    content = {"name": "Alice", "age": 22}
    response = mock_response(content)
    upstream_response = UpstreamResponse(response)

    student = deserialize_or_502(upstream_response, Student, many=False)
    assert isinstance(student, Student)
    assert student.name == "Alice"
    assert student.age == 22


def test_deserialize_or_502_supports_list_deserialization():
    content = [{"name": "Bob", "age": 20}, {"name": "Carol", "age": 25}]
    response = mock_response(content)
    upstream_response = UpstreamResponse(response)

    students = deserialize_or_502(upstream_response, Student, many=True)
    assert isinstance(students, list)
    assert len(students) == 2
    assert all(isinstance(s, Student) for s in students)
    assert students[0].name == "Bob"
    assert students[1].name == "Carol"


def test_deserialize_or_502_gives_502_on_downstream_non_success_response():
    content = {"detail": "Resource not found"}
    response = mock_response(content, status_code=status.HTTP_404_NOT_FOUND)
    upstream_response = UpstreamResponse(response)

    with pytest.raises(HTTPException) as exc_info:
        deserialize_or_502(upstream_response, Student)

    assert exc_info.value.status_code == status.HTTP_502_BAD_GATEWAY
    assert (
        str(exc_info.value.detail) == "ABC API call returned a 404: Resource not found."
    )
