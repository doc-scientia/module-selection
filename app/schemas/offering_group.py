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
    min: int = Field(nullable=False)
    max: int = Field(nullable=False)
    degree_regulations: list["DegreeRegulations"] = Relationship(  # type: ignore
        back_populates="offering_group"
    )


class OfferingGroupRead(SQLModel):
    id: int
    label: OfferingGroupLabel
