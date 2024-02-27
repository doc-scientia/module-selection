from datetime import datetime
from enum import auto

from sqlalchemy import UniqueConstraint
from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from app.utils.SQLModelStrEnum import SQLModelStrEnum


class ModuleSelectionStatus(SQLModelStrEnum):
    CLOSED = auto()
    USE_PERIODS = auto()

    @classmethod
    def members(cls) -> list[str]:
        return [e.value for e in cls]


class SelectionPeriod(SQLModel, table=True):
    __tablename__ = "selection_period"
    id: int = Field(primary_key=True)
    start: datetime = Field(nullable=False, default_factory=datetime.now)
    end: datetime = Field(nullable=False, default_factory=datetime.now)
    configuration_id: int = Field(nullable=False, foreign_key="configuration.id")
    configuration: "Configuration" = Relationship(back_populates="periods")


class SelectionPeriodRead(SQLModel):
    id: int
    start: datetime
    end: datetime


class SelectionPeriodWrite(SQLModel):
    start: datetime
    end: datetime


# -----------------------------------------------
class Configuration(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("year"),)
    id: int = Field(primary_key=True)
    year: str = Field(nullable=False, max_length=10)
    status: ModuleSelectionStatus = Field(
        sa_column=Column(
            Enum(ModuleSelectionStatus, name="module_selection_status"), nullable=False
        )
    )
    periods: list[SelectionPeriod] = Relationship(
        back_populates="configuration",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )


class ConfigurationRead(SQLModel):
    id: int
    status: ModuleSelectionStatus
    periods: list[SelectionPeriodRead]


class ConfigurationWrite(SQLModel):
    status: ModuleSelectionStatus
