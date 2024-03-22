from .configurations import Configuration, SelectionPeriod
from .enrolments import Enrolment
from .external_modules import ExternalModuleChoice, ExternalModuleOnOffer
from .internal_modules import (
    CohortRegulations,
    InternalModuleChoice,
    InternalModuleOnOffer,
)

models = (
    Enrolment,
    Configuration,
    SelectionPeriod,
    ExternalModuleOnOffer,
    ExternalModuleChoice,
    InternalModuleOnOffer,
    CohortRegulations,
    InternalModuleChoice,
)
