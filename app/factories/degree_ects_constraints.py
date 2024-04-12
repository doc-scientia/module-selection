import string

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.schemas import DegreeECTSConstraints


class DegreeECTSConstraintsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = DegreeECTSConstraints
        sqlalchemy_session_persistence = "commit"

    year = factory.Faker("year")
    degree: str = factory.Faker(
        "pystr_format", string_format="##?", letters=string.ascii_uppercase
    )
    min = factory.Faker("pyfloat", min_value=40, max_value=50)
    max = factory.Faker("pyfloat", min_value=55, max_value=60)
