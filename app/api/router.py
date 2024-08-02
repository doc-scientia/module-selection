from fastapi import APIRouter, Depends, Request

from app.dependencies.main import get_settings
from app.schemas.status import Status
from app.settings import Settings

api_router = APIRouter()


@api_router.get("/status", tags=["status"], response_model=Status, summary="Retrieve API Status",
                description="""
Perform status check to determine whether the API is up and running.

And then says Hello World, and then says foobar.


**Access**: Unrestricted.
    """, )
def get_status(
        request: Request,
        settings: Settings = Depends(get_settings),
):
    """
    Status check endpoint to determine that the API is up and running

    ACCESS: Unrestricted
    """

    return {
        "status": "Module Subscriptions alive",
        "version": request.app.version,
        "environment": settings.environment,
        "testing": settings.testing,
    }
