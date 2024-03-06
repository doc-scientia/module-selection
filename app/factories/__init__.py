from typing import Sequence, Type

from factory.alchemy import SQLAlchemyModelFactory

from app.factories.configuration import ConfigurationFactory, SelectionPeriodFactory
from app.factories.external_modules import (
    ExternalModuleChoiceFactory,
    ExternalModuleOnOfferFactory,
)
from app.factories.module_subscriptions import EnrolmentFactory

all_factories: Sequence[Type[SQLAlchemyModelFactory]] = [
    EnrolmentFactory,
    ConfigurationFactory,
    SelectionPeriodFactory,
    ExternalModuleChoiceFactory,
    ExternalModuleOnOfferFactory,
]
