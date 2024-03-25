import string

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.schemas.internal_modules import (
    CohortRegulations,
    InternalModuleChoice,
    InternalModuleOnOffer,
    OfferingGroup,
)


class InternalModuleOnOfferFactory(SQLAlchemyModelFactory):
    class Meta:
        model = InternalModuleOnOffer
        sqlalchemy_session_persistence = "commit"

    title: str = factory.Faker("sentence", nb_words=3)
    year: str = factory.Faker("short_year")
    code: str = factory.Faker(
        "pystr_format", string_format="#####", letters=string.ascii_uppercase
    )
    description: str = factory.Faker("text")
    terms: list[int] = [1, 2, 3]

    @factory.post_generation
    def with_regulations(
        self: InternalModuleOnOffer,
        create: bool,
        regulations: int | list[dict],
        **kwargs
    ) -> None:
        if create and regulations:
            if isinstance(regulations, int):
                for n in range(regulations):
                    CohortRegulationsFactory(module=self)
            if isinstance(regulations, list):
                for r in regulations:
                    CohortRegulationsFactory(module=self, **r)


class CohortRegulationsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = CohortRegulations
        sqlalchemy_session_persistence = "commit"

    cohort: str = factory.Faker(
        "pystr_format", string_format="#?", letters=string.ascii_uppercase
    )
    ects: int = factory.Faker("pyint", min_value=5, max_value=30)
    exam_component: int = factory.Faker("pyint", min_value=1, max_value=10)
    cw_component: int = factory.Faker("pyint", min_value=1, max_value=10)
    offering_group: OfferingGroup = factory.Faker("offering_group_label")

    @factory.post_generation
    def with_enrollments(
        self: CohortRegulations, create: bool, enrollments: int | list[dict], **kwargs
    ) -> None:
        if create and enrollments:
            if isinstance(enrollments, int):
                for n in range(enrollments):
                    InternalModuleChoiceFactory(cohort_regulations=self)
            if isinstance(enrollments, list):
                for e in enrollments:
                    InternalModuleChoiceFactory(cohort_regulations=self, **e)


class InternalModuleChoiceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = InternalModuleChoice
        sqlalchemy_session_persistence = "commit"

    username: str = factory.Faker("pystr_format", string_format="###???")
