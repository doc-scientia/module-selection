import string

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.factories.offering_group import OfferingGroupFactory
from app.schemas.internal_modules import (
    DegreeRegulations,
    InternalModuleChoice,
    InternalModuleOnOffer,
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
    terms: list[int] = factory.Faker("terms")

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
                    DegreeRegulationsFactory(module=self)
            if isinstance(regulations, list):
                for r in regulations:
                    DegreeRegulationsFactory(module=self, **r)


class DegreeRegulationsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = DegreeRegulations
        sqlalchemy_session_persistence = "commit"

    degree: str = factory.Faker(
        "pystr_format", string_format="##?", letters=string.ascii_uppercase
    )
    ects: float = factory.Faker("pyfloat", min_value=5, max_value=30)
    exam_component: int = factory.Faker("pyint", min_value=1, max_value=10)
    cw_component: int = factory.Faker("pyint", min_value=1, max_value=10)
    offering_group = factory.SubFactory(OfferingGroupFactory)

    @factory.post_generation
    def with_enrollments(
        self: DegreeRegulations, create: bool, enrollments: int | list[dict], **kwargs
    ) -> None:
        if create and enrollments:
            if isinstance(enrollments, int):
                for n in range(enrollments):
                    InternalModuleChoiceFactory(degree_regulations=self)
            if isinstance(enrollments, list):
                for e in enrollments:
                    InternalModuleChoiceFactory(degree_regulations=self, **e)


class InternalModuleChoiceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = InternalModuleChoice
        sqlalchemy_session_persistence = "commit"

    username: str = factory.Faker("pystr_format", string_format="###???")
