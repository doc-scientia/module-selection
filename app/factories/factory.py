import random

import factory
from faker.providers import BaseProvider, internet, job, lorem, person, python

from app.schemas.configurations import ModuleSelectionStatus
from app.schemas.internal_modules import TimetableConstraint
from app.schemas.offering_group import OfferingGroupLabel

TERMS = (1, 2, 3)


class ShortYear(BaseProvider):
    def short_year(self) -> str:
        return random.choice(["1920", "2021", "2122", "2223", "2324"])  # nosec


class SelectionStatus(BaseProvider):
    def selection_status(self) -> str:
        return random.choice(ModuleSelectionStatus.members())  # nosec


class OfferingGroupName(BaseProvider):
    def offering_group_label(self) -> str:
        return random.choice(OfferingGroupLabel.members())  # nosec


class Terms(BaseProvider):
    def terms(self) -> list[int]:
        subset_length = random.randint(1, 3)  # nosec
        return random.sample(TERMS, subset_length)  # nosec


class TimetableGroup(BaseProvider):
    def timetable_constraint(self) -> str:
        return random.choice(TimetableConstraint.members())  # nosec


factory.Faker.add_provider(python)
factory.Faker.add_provider(lorem)
factory.Faker.add_provider(internet)
factory.Faker.add_provider(person)
factory.Faker.add_provider(job)
factory.Faker.add_provider(ShortYear)
factory.Faker.add_provider(SelectionStatus)
factory.Faker.add_provider(OfferingGroupName)
factory.Faker.add_provider(Terms)
factory.Faker.add_provider(TimetableGroup)
