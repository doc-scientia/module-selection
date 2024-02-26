from fastapi import FastAPI

from app.api.configuration import module_selection_configuration
from app.api.module_subscriptions import module_router
from app.api.router import api_router

tags_metadata = [
    {
        "name": "status",
        "description": "API heartbeat",
    },
    {"name": "module subscriptions", "description": "Module Subscriptions"},
    {"name": "configurations", "description": "Module Selection Configurations"},
]


def create_application() -> FastAPI:
    rest_api: FastAPI = FastAPI(
        title="Module Subscriptions API",
        description=(
            "API for module subscriptions, Dept. of Computing, Imperial College London"
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
    rest_api.include_router(module_router)
    rest_api.include_router(module_selection_configuration)

    return rest_api
