from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory

from app.dependencies.main import get_session
from app.factories.factory import factory
from app.schemas.configurations import (
    Configuration,
    ModuleSelectionStatus,
    SelectionPeriod,
)


class SelectionPeriodFactory(SQLAlchemyModelFactory):
    class Meta:
        model = SelectionPeriod
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    start: datetime = factory.Faker(
        "date_time_this_month", before_now=True, after_now=False
    )
    end: datetime = factory.Faker(
        "date_time_this_month", before_now=False, after_now=True
    )


class ConfigurationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Configuration
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "commit"

    year: str = factory.Faker("short_year")
    status: ModuleSelectionStatus = factory.Faker("selection_status")

    @factory.post_generation
    def with_periods(self, create, periods: int | list[dict], **kwargs):
        if create and periods:
            if isinstance(periods, int):
                for _ in range(periods):
                    SelectionPeriodFactory(configuration=self)
            else:
                for p in periods:
                    SelectionPeriodFactory(configuration=self, **p)
