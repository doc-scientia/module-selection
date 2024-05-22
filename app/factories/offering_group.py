import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.schemas.constraints import OfferingGroup, OfferingGroupLabel


class OfferingGroupFactory(SQLAlchemyModelFactory):
    class Meta:
        model = OfferingGroup
        sqlalchemy_session_persistence = "commit"

    label: OfferingGroupLabel = factory.Faker("offering_group_label")
    year = factory.Faker("year")
    min = factory.Faker("pyfloat", min_value=1, max_value=5, right_digits=2)
    max = factory.Faker("pyfloat", min_value=6, max_value=10, right_digits=2)
