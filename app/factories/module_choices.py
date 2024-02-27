from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory

from app.dependencies import get_session
from app.factories.factory import factory
from app.schemas.module_choices import ExternalModuleChoice


class ExternalModuleChoiceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ExternalModuleChoice
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    year: str = factory.Faker("short_year")
    module_code: str = factory.Faker("pystr_format", string_format="#######")
    timestamp: datetime = factory.Faker(
        "date_time_this_month", before_now=True, after_now=False
    )
    username: str = factory.Faker("pystr_format", string_format="###???")
