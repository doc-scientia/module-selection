from typing import Sequence, Type

from factory.alchemy import SQLAlchemyModelFactory

from app.factories.configuration import ConfigurationFactory, SelectionPeriodFactory
from app.factories.external_module_on_offer import ExternalModuleOnOfferFactory
from app.factories.module_choices import ExternalModuleChoiceFactory
from app.factories.module_subscriptions import EnrolmentFactory

all_factories: Sequence[Type[SQLAlchemyModelFactory]] = [
    EnrolmentFactory,
    ConfigurationFactory,
    SelectionPeriodFactory,
    ExternalModuleChoiceFactory,
    ExternalModuleOnOfferFactory,
]
