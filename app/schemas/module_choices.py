from datetime import datetime, timezone
from enum import auto

from sqlalchemy import DateTime, UniqueConstraint, func
from sqlmodel import ARRAY, Column, Enum, Field, Integer, SQLModel

from app.utils.SQLModelStrEnum import SQLModelStrEnum


class ModuleChoiceApprovalStatus(SQLModelStrEnum):
    APPROVED = auto()
    REJECTED = auto()
    PENDING = auto()

    @classmethod
    def members(cls) -> list[str]:
        return [e.value for e in cls]


class ExternalModuleChoice(SQLModel, table=True):
    __tablename__ = "external_module_choice"
    __table_args__ = (UniqueConstraint("year", "module_code", "username"),)
    id: int = Field(primary_key=True)
    year: str = Field(max_length=10)
    module_code: str
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.timezone("UTC", func.current_timestamp()),
            nullable=False,
        )
    )
    username: str
    status: ModuleChoiceApprovalStatus = Field(
        sa_column=Column(
            Enum(ModuleChoiceApprovalStatus, name="module_choice_approval_status"),
            server_default=ModuleChoiceApprovalStatus.PENDING.value,
            nullable=False,
        )
    )
    reviewed_on: datetime | None
    reviewed_by: str | None


class ExternalModuleChoiceRead(SQLModel):
    id: int
    year: str
    module_code: str
    timestamp: datetime
    username: str
    status: ModuleChoiceApprovalStatus
    reviewed_on: datetime | None
    reviewed_by: str | None

    def dict(self, **kwargs):
        obj_dict = super().dict(**kwargs)
        for field in ["timestamp", "reviewed_on"]:
            if current_value := getattr(self, field):
                obj_dict[field] = current_value.replace(tzinfo=timezone.utc).isoformat()
        return obj_dict


class ExternalModuleChoiceUpdate(SQLModel):
    status: ModuleChoiceApprovalStatus


class ExternalModuleChoiceWrite(SQLModel):
    module_code: str


class ExternalModuleOnOffer(SQLModel, table=True):
    __tablename__ = "external_module_on_offer"
    id: int = Field(primary_key=True)
    title: str = Field(nullable=False)
    code: str = Field(max_length=30, nullable=False)
    terms: list[int] = Field(default=None, sa_column=Column(ARRAY(Integer())))
    ects: int = Field(nullable=False)
