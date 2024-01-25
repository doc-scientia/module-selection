import string
from datetime import date

from factory.alchemy import SQLAlchemyModelFactory

from app.dependencies import get_session
from app.factories.factory import factory
from app.schemas.tutoring_sessions import TutoringSession, TutoringSessionAttendance


class TutoringSessionAttendanceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = TutoringSessionAttendance
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    username: str = factory.Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
    present: bool = factory.Faker("pybool")


class TutoringSessionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = TutoringSession
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    group: str = factory.Faker(
        "pystr_format", string_format="??? #", letters=string.ascii_uppercase
    )
    date: date = factory.Faker("date_this_month")
    year: str = factory.Faker("short_year")

    @factory.post_generation
    def with_attendances(
        self: TutoringSession, create: bool, attendances: int | list[dict] = 3, **kwargs
    ) -> None:
        if create and attendances:
            if isinstance(attendances, int):
                for n in range(attendances):
                    TutoringSessionAttendanceFactory(
                        tutoring_session_id=self.id,
                    )
            if isinstance(attendances, list):
                for a in attendances:
                    TutoringSessionAttendanceFactory(tutoring_session_id=self.id, **a)
