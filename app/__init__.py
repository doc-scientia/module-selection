from fastapi import FastAPI

from app.api.personal import personal_router
from app.api.personal_tutor_meetings import pt_meetings_router
from app.api.router import api_router
from app.api.student_tutoring_sessions import student_tutoring_sessions_router
from app.api.tutoring_sessions import sessions_router

tags_metadata = [
    {
        "name": "status",
        "description": "API heartbeat",
    },
    {"name": "tutoring-sessions", "description": "PPT/PMT/MMT tutoring sessions"},
]


def create_application() -> FastAPI:
    rest_api: FastAPI = FastAPI(
        title="Tutoring API",
        description=(
            "API for tracking tutoring activities, Dept. of Computing, Imperial College London"
        ),
        version="1.0",
        contact={
            "name": "Doc EdTech Lab",
            "url": "https://edtech.pages.doc.ic.ac.uk/",
            "email": "doc-edtech@ic.ac.uk",
        },
        openapi_tags=tags_metadata,
        docs_url="/",
    )
    rest_api.include_router(api_router)
    rest_api.include_router(sessions_router)
    rest_api.include_router(personal_router)
    rest_api.include_router(pt_meetings_router)
    rest_api.include_router(student_tutoring_sessions_router)

    return rest_api
