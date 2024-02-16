from datetime import datetime

from sqlalchemy import func
from sqlalchemy.types import DateTime
from sqlmodel import Column, Field, SQLModel


class Enrolment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    student_username: str = Field(nullable=False, max_length=10)
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.timezone("UTC", func.current_timestamp()),
            nullable=False,
        )
    )
    enrolment_type: str = Field(nullable=False)
    module_code: str = Field(nullable=False)
    year: str = Field(nullable=False, max_length=10)


class ModuleSubscription(SQLModel):
    module_code: str


class EnrolmentRead(SQLModel):
    student_username: str
    module_code: str
    enrolment_type: str
    timestamp: datetime
