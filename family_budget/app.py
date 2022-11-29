from logging.config import dictConfig
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from family_budget.core.config import get_settings
from family_budget.routers.v1 import api_router

settings = get_settings()


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, openapi_url="/openapi.json")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(api_router)
    return _app


app = get_application()
