from sqlmodel import Field, SQLModel


class DegreeECTSConstraints(SQLModel, table=True):
    __tablename__ = "degree_ects_constraints"
    id: int = Field(primary_key=True)
    year: str = Field(nullable=False)
    degree: str = Field(nullable=False)
    min: float = Field(nullable=False)
    max: float = Field(nullable=False)
