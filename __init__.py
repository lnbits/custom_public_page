from fastapi import APIRouter

from .crud import db
from .views import custom_public_page_generic_router
from .views_api import custom_public_page_api_router

custom_public_page_ext: APIRouter = APIRouter(
    prefix="/custom_public_page", tags=["CustomPublicPage"]
)
custom_public_page_ext.include_router(custom_public_page_generic_router)
custom_public_page_ext.include_router(custom_public_page_api_router)


custom_public_page_static_files = [
    {
        "path": "/custom_public_page/static",
        "name": "custom_public_page_static",
    }
]


def custom_public_page_stop():
    return None


def custom_public_page_start():
    return None


__all__ = [
    "db",
    "custom_public_page_ext",
    "custom_public_page_start",
    "custom_public_page_static_files",
    "custom_public_page_stop",
]
