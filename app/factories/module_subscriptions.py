import string
from datetime import date

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.dependencies.main import get_session
from app.schemas import Enrolment


class EnrolmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Enrolment
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    student_username: str = factory.Faker(
        "pystr_format", string_format="????##", letters=string.ascii_lowercase
    )
    module_code: str = factory.Faker(
        "pystr_format", string_format="#####", letters=string.ascii_lowercase
    )
    enrolment_date: date = factory.Faker(
        "date_this_year", before_today=True, after_today=False
    )

    enrolment_type: str = factory.Faker(
        "pystr_format", string_format="??????", letters=string.ascii_lowercase
    )

    timestamp: date = factory.Faker(
        "date_this_year", before_today=True, after_today=False
    )

    year: str = factory.Faker(
        "pystr_format", string_format="####", letters=string.ascii_lowercase
    )
