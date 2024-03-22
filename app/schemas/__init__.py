from .configurations import Configuration, SelectionPeriod
from .external_modules import ExternalModuleChoice, ExternalModuleOnOffer
from .internal_modules import (
    CohortRegulations,
    InternalModuleChoice,
    InternalModuleOnOffer,
)

models = (
    Configuration,
    SelectionPeriod,
    ExternalModuleOnOffer,
    ExternalModuleChoice,
    InternalModuleOnOffer,
    CohortRegulations,
    InternalModuleChoice,
)
