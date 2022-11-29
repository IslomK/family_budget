from fastapi import APIRouter, Depends
from pydantic import BaseModel

from family_budget.core.config import Settings, get_settings

router = APIRouter()


class HealthCheckResponse(BaseModel):
    service: str
    environment: str
    version: str


@router.get("/healthcheck", tags=["healthcheck"], response_model=HealthCheckResponse)
async def healthcheck(settings: Settings = Depends(get_settings)) -> HealthCheckResponse:
    return HealthCheckResponse(
        service=settings.PROJECT_NAME, environment=settings.ENVIRONMENT, version="v1"
    )
