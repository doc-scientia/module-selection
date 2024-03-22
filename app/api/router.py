from fastapi import APIRouter, Depends, Request

from app.dependencies.main import get_settings
from app.schemas.status import Status
from app.settings import Settings

api_router = APIRouter()


@api_router.get("/status", tags=["status"], response_model=Status)
def get_status(
    request: Request,
    settings: Settings = Depends(get_settings),
):
    return {
        "status": "Module Subscriptions alive",
        "version": request.app.version,
        "environment": settings.environment,
        "testing": settings.testing,
    }
