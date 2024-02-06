from typing import Sequence, Type

from factory.alchemy import SQLAlchemyModelFactory

from app.factories.module_subscriptions import EnrolmentFactory

all_factories: Sequence[Type[SQLAlchemyModelFactory]] = [
    EnrolmentFactory,
]
