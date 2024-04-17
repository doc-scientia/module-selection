from sqlmodel import Field, SQLModel


class Admin(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(nullable=False)
