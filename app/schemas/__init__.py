from .configurations import Configuration, SelectionPeriod
from .external_modules import ExternalModuleChoice, ExternalModuleOnOffer
from .internal_modules import (
    CohortRegulations,
    InternalModuleChoice,
    InternalModuleOnOffer,
)
from .offering_group import OfferingGroup

models = (
    Configuration,
    SelectionPeriod,
    ExternalModuleOnOffer,
    ExternalModuleChoice,
    InternalModuleOnOffer,
    OfferingGroup,
    CohortRegulations,
    InternalModuleChoice,
)
