from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class TutoringSessionAttendanceBase(SQLModel):
    username: str
    present: bool


class TutoringSessionBase(SQLModel):
    group: str
    date: date


class StudentTutoringSessionAttendanceRead(TutoringSessionBase):
    id: int
    present: bool


class TutoringSessionAttendance(TutoringSessionAttendanceBase, table=True):
    __tablename__ = "tutoring_session_attendance"
    id: int = Field(primary_key=True)
    tutoring_session_id: int = Field(index=True, foreign_key="tutoring_session.id")
    tutoring_session: "TutoringSession" = Relationship(back_populates="attendances")


class TutoringSession(TutoringSessionBase, table=True):
    __tablename__ = "tutoring_session"
    id: int = Field(primary_key=True)
    year: str
    attendances: list[TutoringSessionAttendance] = Relationship(
        back_populates="tutoring_session",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )


class TutoringSessionAttendanceRead(TutoringSessionAttendanceBase):
    id: int


class TutoringSessionWrite(TutoringSessionBase):
    attendances: list[TutoringSessionAttendanceBase] = Field(default=[])


class TutoringSessionRead(TutoringSessionBase):
    id: int
    year: str
    attendances: list[TutoringSessionAttendanceRead] = Field(default=[])
