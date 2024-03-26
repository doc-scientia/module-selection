from sqlalchemy import Column, Enum
from sqlmodel import Field, SQLModel

from app.schemas.internal_modules import OfferingGroup


class OfferingGroupConstraint(SQLModel, table=True):
    __tablename__ = "offering_group_constraint"
    id: int = Field(primary_key=True)
    year: str = Field(nullable=False)
    offering_group: OfferingGroup = Field(
        sa_column=Column(
            Enum(OfferingGroup, name="offering_group_label"),
            nullable=False,
        )
    )
    min: int = Field(nullable=False)
    max: int = Field(nullable=False)
