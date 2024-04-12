from .configurations import Configuration, SelectionPeriod
from .degree_ects_constraints import DegreeECTSConstraints
from .external_modules import ExternalModuleChoice, ExternalModuleOnOffer
from .internal_modules import (
    DegreeRegulations,
    InternalModuleChoice,
    InternalModuleOnOffer,
)
from .offering_group import OfferingGroup

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
