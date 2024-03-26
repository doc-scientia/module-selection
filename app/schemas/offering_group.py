from sqlalchemy import Column, Enum
from sqlmodel import Field, SQLModel

from app.schemas.internal_modules import OfferingGroupLabel


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
