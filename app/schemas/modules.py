from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class Module(SQLModel, table=True):
    __tablename__ = "module"
    id: int = Field(primary_key=True, nullable=False)
    module_code: str = Field(nullable=False)
    year: str = Field(nullable=False)


class Enrolment(SQLModel, table=True):
    __tablename__ = "enrolments"
    id: int = Field(primary_key=True)
    student_username: str = Field(nullable=False)
    module: int = Field(foreign_key="module.id", nullable=False)
    enrolment_date: date = Field(nullable=False)
    enrolment_type: str = Field(nullable=False)
