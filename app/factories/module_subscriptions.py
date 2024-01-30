import string
from datetime import date
from enum import Enum

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.dependencies import get_session
from app.schemas import Enrolment, Module


class ModuleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Module
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    module_code: str = factory.Faker(
        "pystr_format", string_format="#####", letters=string.ascii_lowercase
    )
    # todo:  year: str = factory.Faker("short_year")
    year: str = "2324"


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
