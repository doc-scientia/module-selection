from datetime import date, datetime

from sqlmodel import Field, SQLModel


class PersonalTutoringMeeting(SQLModel, table=True):
    __tablename__ = "personal_tutoring_meeting"
    id: int = Field(primary_key=True)
    year: str = Field(nullable=False)
    meeting_date: date = Field(nullable=False)
    tutee: str = Field(nullable=False)
    tutor: str = Field(nullable=False)
    label: str = Field(nullable=False)
    timestamp: datetime = Field(nullable=False, default_factory=datetime.utcnow)


class PersonalTutorMeetingRead(SQLModel):
    year: str
    meeting_date: date
    tutee: str
    tutor: str
    label: str

    class Config:
        schema_extra = {
            "example": {
                "year": "2324",
                "meeting_date": "2023-11-02",
                "tutor": "adumble",
                "tutee": "hpotter",
                "label": "Catch up on horcruxes",
            }
        }


class PersonalTutorMeetingWrite(SQLModel):
    meeting_date: date
    tutee: str
    label: str


class PersonalTutorMeetingUpdate(SQLModel):
    meeting_date: str | None = None
    label: str | None = None
