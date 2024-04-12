from datetime import datetime, timezone
from enum import auto

from sqlalchemy import DateTime, Enum, UniqueConstraint, func
from sqlmodel import ARRAY, Column, Field, Integer, Relationship, SQLModel

from app.schemas.offering_group import OfferingGroupRead
from app.utils.SQLModelStrEnum import SQLModelStrEnum


class ExamTimetableConstraint(SQLModelStrEnum):
    Tx101 = auto()
    Tx102 = auto()
    Tx103 = auto()
    Tx104 = auto()
    Tx105 = auto()
    Tx106 = auto()
    Tx107 = auto()
    Tx108 = auto()
    Tx109 = auto()
    Tx201 = auto()
    Tx202 = auto()
    Tx203 = auto()
    Tx204 = auto()
    Tx205 = auto()
    Tx206 = auto()
    Tx207 = auto()
    Tx208 = auto()
    Tx209 = auto()


class InternalModuleOnOffer(SQLModel, table=True):
    __tablename__ = "internal_module_on_offer"
    id: int = Field(primary_key=True)
    year: str = Field(nullable=False)
    title: str = Field(nullable=False)
    code: str = Field(max_length=30, nullable=False)
    description: str
    terms: list[int] = Field(default=None, sa_column=Column(ARRAY(Integer())))
    exam_timetable_constraint: ExamTimetableConstraint = Field(
        sa_column=Column(
            Enum(ExamTimetableConstraint, name="exam_timetable_constraint"),
        )
    )
    regulations: list["DegreeRegulations"] = Relationship(
        back_populates="module",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )


class DegreeRegulations(SQLModel, table=True):
    __tablename__ = "degree_regulations"
    id: int = Field(primary_key=True)
    degree: str = Field(nullable=False)
    ects: int = Field(nullable=False)
    exam_component: int = Field(nullable=False)
    cw_component: int = Field(nullable=False)
    module_id: int = Field(index=True, foreign_key="internal_module_on_offer.id")
    module: InternalModuleOnOffer = Relationship(back_populates="regulations")
    enrollments: list["InternalModuleChoice"] = Relationship(
        back_populates="degree_regulations",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    offering_group_id: int = Field(foreign_key="offering_group.id", nullable=False)
    offering_group: "OfferingGroup" = Relationship(back_populates="degree_regulations")  # type: ignore


class InternalModuleChoice(SQLModel, table=True):
    __tablename__ = "internal_module_choice"
    __table_args__ = (UniqueConstraint("degree_regulations_id", "username"),)
    id: int = Field(primary_key=True)
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.timezone("UTC", func.current_timestamp()),
            nullable=False,
        )
    )
    username: str
    degree_regulations_id: int = Field(index=True, foreign_key="degree_regulations.id")
    degree_regulations: DegreeRegulations = Relationship(back_populates="enrollments")


class DegreeRegulationsRead(SQLModel):
    id: int
    module_id: int
    degree: str
    ects: int
    exam_component: int
    cw_component: int
    offering_group: OfferingGroupRead


class InternalModuleOnOfferRead(SQLModel):
    id: int
    year: str
    title: str
    code: str
    description: str
    terms: list[int]
    regulations: list[DegreeRegulationsRead]


class InternalModuleChoiceRead(SQLModel):
    id: int
    degree_regulations: DegreeRegulationsRead
    timestamp: datetime
    username: str

    def dict(self, **kwargs):
        obj_dict = super().dict(**kwargs)
        for field in ["timestamp"]:
            if current_value := getattr(self, field):
                obj_dict[field] = current_value.replace(tzinfo=timezone.utc).isoformat()
        return obj_dict


class InternalModuleChoiceWrite(SQLModel):
    module_code: str
    degree: str
