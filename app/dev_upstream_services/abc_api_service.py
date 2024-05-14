import json
from dataclasses import dataclass

from app.doc_upstream_services.abc.api_service import deserialize_or_502
from app.doc_upstream_services.abc.schemas import Student
from app.doc_upstream_services.response_wrappers import UpstreamResponse
from app.protocols import AbcUpstreamService


@dataclass
class DummyResponse:
    content: str | None
    status_code: int = 200
    headers: list | None = None

    def json(self):
        return json.loads(self.content)


class DummyAbcAPIService(AbcUpstreamService):
    def get_staff(
        self,
        year: str,
        login: str,
        proxied_user: str | None = None,
    ) -> UpstreamResponse:
        FAKE_PHD_STAFF = {
            "login": "adumble",
            "year": "2223",
            "email": "adumble@ic.ac.uk",
            "firstname": "Albus",
            "lastname": "Dumbledore",
            "salutation": "Prof",
            "role_in_department": "staff",
        }

        return UpstreamResponse(
            response=DummyResponse(
                content=json.dumps(FAKE_PHD_STAFF if login == "adumble" else [])
            )
        )

    def get_student(
        self, year: str, login: str, proxied_user: str | None = None
    ) -> Student:
        details_404 = {"detail": "Student not found"}

        fake_students = {
            "hpotter": {
                "login": "hpotter",
                "year": "2324",
                "email": "harry.potter@ic.ac.uk",
                "firstname": "Harry",
                "lastname": "Potter",
                "salutation": "Mr",
                "role_in_department": "student",
                "cohort": "c1",
                "cid": "0999999",
                "exam_class": "bm2",
                "degree_code": "mcai",
                "degree_year": "mcai1",
                "student_status": "Normal",
                "entry_year": 2023,
                "fee_status": "Home",
            }
        }

        res = UpstreamResponse(
            response=DummyResponse(
                status_code=200 if login in fake_students else 404,
                content=json.dumps(
                    fake_students[login] if login in fake_students else details_404
                ),
            )
        )
        return deserialize_or_502(res, Student)
