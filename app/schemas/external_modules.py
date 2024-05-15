from datetime import datetime, timezone
from enum import auto

from sqlalchemy import DateTime, UniqueConstraint, func
from sqlmodel import ARRAY, Column, Enum, Field, Integer, Relationship, SQLModel

from app.utils.SQLModelStrEnum import SQLModelStrEnum


class ModuleChoiceApprovalStatus(SQLModelStrEnum):
    APPROVED = auto()
    REJECTED = auto()
    PENDING = auto()

    @classmethod
    def members(cls) -> list[str]:
        return [e.value for e in cls]


class ExternalModuleOnOffer(SQLModel, table=True):
    __tablename__ = "external_module_on_offer"
    id: int = Field(primary_key=True)
    year: str = Field(nullable=False)
    title: str = Field(nullable=False)
    code: str = Field(max_length=30, nullable=False)
    terms: list[int] = Field(default=None, sa_column=Column(ARRAY(Integer())))
    ects: int = Field(nullable=False)
    applications: list["ExternalModuleChoice"] = Relationship(
        back_populates="external_module",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                [
                    {
                        "id": 77,
                        "year": "2324",
                        "title": "Business Studies",
                        "code": "BUSI60005",
                        "terms": [1, 2],
                        "ects": 7.5,
                    }
                ]
            ]
        }
    }


class ExternalModuleRead(SQLModel):
    id: int
    title: str
    code: str
    terms: list[int]
    ects: int


class ExternalModuleChoice(SQLModel, table=True):
    __tablename__ = "external_module_choice"
    __table_args__ = (UniqueConstraint("external_module_id", "username"),)
    id: int = Field(primary_key=True)
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
    external_module_id: int = Field(
        index=True, foreign_key="external_module_on_offer.id"
    )
    external_module: ExternalModuleOnOffer = Relationship(back_populates="applications")


class ExternalModuleChoiceRead(SQLModel):
    id: int
    external_module_id: int
    timestamp: datetime
    username: str
    status: ModuleChoiceApprovalStatus
    reviewed_on: datetime | None
    reviewed_by: str | None

    class Config:
        json_schema_extra = {
            "example": [
                [
                    {
                        "id": 77,
                        "external_module_id": 99,
                        "timestamp": "2024-05-09T15:10:07.370Z",
                        "username": "adumble",
                        "status": "APPROVED",
                        "reviewed_on": "2024-05-09T15:10:07.370Z",
                        "reviewed_by": "adumble",
                    }
                ]
            ]
        }

        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat()
            if dt
            else None,
        }

        model_config = {
            "json_schema_extra": {
                "examples": [
                    [
                        {
                            "id": 77,
                            "external_module_id": 99,
                            "timestamp": "2024-05-09T15:10:07.370Z",
                            "username": "adumble",
                            "status": "APPROVED",
                            "reviewed_on": "2024-05-09T15:10:07.370Z",
                            "reviewed_by": "adumble",
                        }
                    ]
                ]
            }
        }


class ExternalModuleChoiceUpdate(SQLModel):
    status: ModuleChoiceApprovalStatus


class ExternalModuleChoiceWrite(SQLModel):
    module_code: str
