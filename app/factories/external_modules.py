import string

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.schemas.external_modules import ExternalModuleChoice, ExternalModuleOnOffer


class ExternalModuleOnOfferFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ExternalModuleOnOffer
        sqlalchemy_session_persistence = "commit"

    title: str = factory.Faker("sentence", nb_words=3)
    year: str = factory.Faker("short_year")
    code: str = factory.Faker(
        "pystr_format", string_format="#####", letters=string.ascii_uppercase
    )
    terms: list[int] = [1, 2, 3]
    ects: int = factory.Faker("pyint", min_value=5, max_value=30)

    @factory.post_generation
    def with_applications(
        self: ExternalModuleOnOffer,
        create: bool,
        applications: int | list[dict],
        **kwargs
    ) -> None:
        if create and applications:
            if isinstance(applications, int):
                for n in range(applications):
                    ExternalModuleChoiceFactory(
                        external_module_id=self.id,
                    )
            if isinstance(applications, list):
                for a in applications:
                    ExternalModuleChoiceFactory(external_module_id=self.id, **a)


class ExternalModuleChoiceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ExternalModuleChoice
        sqlalchemy_session_persistence = "commit"

    username: str = factory.Faker("pystr_format", string_format="###???")
