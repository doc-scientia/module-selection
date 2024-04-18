from pydantic import BaseModel


class Student(BaseModel):
    login: str
    degree_year: str
    cohort: str
