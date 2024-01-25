from typing import Sequence, Type

from factory.alchemy import SQLAlchemyModelFactory

from app.factories.pt_meetings import PersonalTutoringMeetingFactory
from app.factories.tutoring_sessions import (
    TutoringSessionAttendanceFactory,
    TutoringSessionFactory,
)

all_factories: Sequence[Type[SQLAlchemyModelFactory]] = [
    TutoringSessionFactory,
    TutoringSessionAttendanceFactory,
    PersonalTutoringMeetingFactory,
]
