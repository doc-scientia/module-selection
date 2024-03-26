import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.schemas.offering_group import OfferingGroup, OfferingGroupLabel


class OfferingGroupFactory(SQLAlchemyModelFactory):
    class Meta:
        model = OfferingGroup
        sqlalchemy_session_persistence = "commit"

    label: OfferingGroupLabel = factory.Faker("offering_group_label")
    year = factory.Faker("year")
    min = factory.Faker("pyint", min_value=1, max_value=5)
    max = factory.Faker("pyint", min_value=6, max_value=10)
