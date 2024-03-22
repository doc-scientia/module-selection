from .configurations import Configuration, SelectionPeriod
from .external_modules import ExternalModuleChoice, ExternalModuleOnOffer
from .internal_modules import (
    CohortRegulations,
    InternalModuleChoice,
    InternalModuleOnOffer,
)
from .offering_group import OfferingGroupConstraint

models = (
    Configuration,
    SelectionPeriod,
    ExternalModuleOnOffer,
    ExternalModuleChoice,
    InternalModuleOnOffer,
    OfferingGroupConstraint,
    CohortRegulations,
    InternalModuleChoice,
)
