from pydantic import BaseModel


class Status(BaseModel):
    """The API Status"""

    status: str
    version: str
    environment: str
    testing: bool
