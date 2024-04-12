from fastapi import FastAPI

from app.api.configuration import module_selection_configuration
from app.api.constraints import constraints_router
from app.api.exernal_module_choices_review import external_module_choices_review_router
from app.api.modules_on_offer import modules_on_offer_router
from app.api.personal import personal_router
from app.api.router import api_router
from app.settings import Settings

tags_metadata = [
    {
        "name": "status",
        "description": "API heartbeat",
    },
    {
        "name": "configuration",
        "description": "Configuration of module selection periods",
    },
    {
        "name": "external module choices review",
        "description": "Approval/rejection of external module choices",
    },
    {
        "name": "personal module choices",
        "description": "Summary and update of personal module choices",
    },
    {"name": "on offer", "description": "List of modules on offer"},
    {
        "name": "constraints",
        "description": "Comprehensive overview of degree constraints (globally and by offering group)",
    },
]


def create_application() -> FastAPI:
    rest_api: FastAPI = FastAPI(
        title="Module Selection API",
        description=(
            "API for module selection, Dept. of Computing, Imperial College London"
        ),
        version="1.0",
        contact={
            "name": "Doc EdTech Lab",
            "url": "https://edtech.pages.doc.ic.ac.uk/",
            "email": "doc-edtech@ic.ac.uk",
        },
        servers=[{"url": Settings().server_url, "description": Settings().environment}],
        openapi_tags=tags_metadata,
        docs_url="/",
    )
    rest_api.include_router(api_router)
    rest_api.include_router(module_selection_configuration)
    rest_api.include_router(external_module_choices_review_router)
    rest_api.include_router(personal_router)
    rest_api.include_router(modules_on_offer_router)
    rest_api.include_router(constraints_router)

    return rest_api
