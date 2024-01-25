import string
from datetime import date

from factory.alchemy import SQLAlchemyModelFactory

from app.dependencies import get_session
from app.factories.factory import factory
from app.schemas.personal_tutoring_meeting import PersonalTutoringMeeting


class PersonalTutoringMeetingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = PersonalTutoringMeeting
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    year: str = factory.Faker("short_year")
    label: str = factory.Faker("text", max_nb_chars=55)
    tutee: str = factory.Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
    tutor: str = factory.Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
    meeting_date: date = factory.Faker(
        "date_time_this_month", before_now=True, after_now=False
    )
