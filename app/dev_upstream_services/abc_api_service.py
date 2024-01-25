import json
from dataclasses import dataclass

from starlette import status

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
    def get_staff_info(
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

    def get_student_info(
        self,
        year: str,
        login: str,
        proxied_user: str | None = None,
    ) -> UpstreamResponse:
        FAKE_PHD_STUDENT = {
            "br99": [
                {
                    "login": "br99",
                    "email": "br99@imperial.ac.uk",
                    "lastname": "Rostenkowski",
                    "firstname": "Bernadette",
                    "salutation": "Dr",
                    "year": "2223",
                    "role_in_department": "phd",
                    "cohort": "r6",
                },
            ],
            "rgeller ": [
                {
                    "login": "rgeller",
                    "firstname": "Ross",
                    "lastname": "Geller",
                    "email_address": "rg123@imperial.ac.uk",
                    "salutation": "Dr",
                    "year": "2223",
                    "role_in_department": "phd",
                    "cohort": "r6",
                }
            ],
        }

        return UpstreamResponse(
            response=DummyResponse(
                content=json.dumps(
                    FAKE_PHD_STUDENT[proxied_user] if proxied_user else []
                )
            )
        )

    def get_tutorial_groups(
        self,
        year: str,
        module_codes: list[str] | None = None,
        numbers: list[int] | None = None,
        types: list[str] | None = None,
        proxied_user: str | None = None,
    ) -> UpstreamResponse:
        return UpstreamResponse(
            response=DummyResponse(
                status_code=status.HTTP_200_OK,
                content=json.dumps(
                    [
                        {
                            "number": 1,
                            "type": "PMT",
                            "tutor": {"login": "adumble"},
                            "uta": {"login": "cdiggory"},
                            "members": [
                                {"login": "hpotter"},
                                {"login": "rweasley"},
                            ],
                        },
                        {
                            "number": 2,
                            "type": "PMT",
                            "tutor": {"login": "rhagrid"},
                            "uta": {"login": "pweasley"},
                            "members": [
                                {"login": "hgranger"},
                                {"login": "dmalfoy"},
                            ],
                        },
                    ]
                ),
            )
        )
