from enum import auto

from sqlalchemy import Column, Enum
from sqlmodel import Field, Relationship, SQLModel

from app.utils.SQLModelStrEnum import SQLModelStrEnum


class OfferingGroupLabel(SQLModelStrEnum):
    OPTIONAL = auto()
    SELECTIVE = auto()


class OfferingGroup(SQLModel, table=True):
    __tablename__ = "offering_group"
    id: int = Field(primary_key=True)
    year: str = Field(nullable=False)
    label: OfferingGroupLabel = Field(
        sa_column=Column(
            Enum(OfferingGroupLabel, name="offering_group_label"),
            nullable=False,
        )
    )
    min: float = Field(nullable=False)
    max: float = Field(nullable=False)
    degree_regulations: list["DegreeRegulations"] = Relationship(  # type: ignore
        back_populates="offering_group"
    )


class OfferingGroupRead(SQLModel):
    id: int
    label: OfferingGroupLabel
    min: float
    max: float


class DegreeECTSConstraints(SQLModel, table=True):
    __tablename__ = "degree_ects_constraints"
    id: int = Field(primary_key=True)
    year: str = Field(nullable=False)
    degree: str = Field(nullable=False)
    min: float = Field(nullable=False)
    max: float = Field(nullable=False)


class DegreeECTSConstraintsRead(SQLModel):
    min: float
    max: float


class ConstraintsRead(SQLModel):
    degree: str
    year: str
    degree_constraints: DegreeECTSConstraintsRead
    offering_group_constraints: list[OfferingGroupRead]
