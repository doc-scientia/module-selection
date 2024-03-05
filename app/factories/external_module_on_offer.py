import string

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.dependencies import get_session
from app.schemas.module_choices import ExternalModuleOnOffer


class ExternalModuleOnOfferFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ExternalModuleOnOffer
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    title: str = factory.Faker("job")
    code: str = factory.Faker(
        "pystr_format", string_format="#####", letters=string.ascii_lowercase
    )
    terms: list[int] = [1, 2, 3]

    ects: int = factory.Faker("pyint", min_value=5, max_value=30)
