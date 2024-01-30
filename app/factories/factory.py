import random

import factory
from faker.providers import BaseProvider, internet, job, lorem, person, python


class ShortYear(BaseProvider):
    def short_year(self) -> str:
        return random.choice(["1920", "2021", "2122", "2223", "2324"])


class Terms(BaseProvider):
    def terms(self) -> str:
        return ",".join(sorted(random.sample("123", random.randint(1, 3))))


class ExerciseType(BaseProvider):
    def exercise_type(self) -> str:
        return random.choice(["CW", "PPT", "PMT", "MMT"])


factory.Faker.add_provider(python)
factory.Faker.add_provider(lorem)
factory.Faker.add_provider(internet)
factory.Faker.add_provider(person)
factory.Faker.add_provider(job)
factory.Faker.add_provider(Terms)
factory.Faker.add_provider(ShortYear)
factory.Faker.add_provider(ExerciseType)
