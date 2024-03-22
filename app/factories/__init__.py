from typing import Sequence, Type

from factory.alchemy import SQLAlchemyModelFactory

from app.factories.configuration import ConfigurationFactory, SelectionPeriodFactory
from app.factories.external_modules import (
    ExternalModuleChoiceFactory,
    ExternalModuleOnOfferFactory,
)
from app.factories.internal_modules import (
    CohortRegulationsFactory,
    InternalModuleChoiceFactory,
    InternalModuleOnOfferFactory,
)

all_factories: Sequence[Type[SQLAlchemyModelFactory]] = [
    ConfigurationFactory,
    SelectionPeriodFactory,
    ExternalModuleChoiceFactory,
    ExternalModuleOnOfferFactory,
    InternalModuleOnOfferFactory,
    CohortRegulationsFactory,
    InternalModuleChoiceFactory,
]
