from .configurations import Configuration, SelectionPeriod
from .constraints import DegreeECTSConstraints, OfferingGroup
from .external_modules import ExternalModuleChoice, ExternalModuleOnOffer
from .internal_modules import (
    DegreeRegulations,
    InternalModuleChoice,
    InternalModuleOnOffer,
)

models = (
    DegreeECTSConstraints,
    Configuration,
    SelectionPeriod,
    ExternalModuleOnOffer,
    ExternalModuleChoice,
    InternalModuleOnOffer,
    OfferingGroup,
    DegreeRegulations,
    InternalModuleChoice,
)
