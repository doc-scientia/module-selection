from datetime import datetime

from sqlmodel import Field, SQLModel


class Enrolment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    student_username: str = Field(nullable=False)
    timestamp: datetime = Field(nullable=False, default_factory=datetime.utcnow)
    enrolment_type: str = Field(nullable=False)
    module_code: str = Field(nullable=False)
    year: str = Field(nullable=False)


class ModuleSubscription(SQLModel):
    module_code: str
