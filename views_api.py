from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.core.models import SimpleStatus, User
from lnbits.db import Filters, Page
from lnbits.decorators import (
    check_user_exists,
    parse_filters,
)
from lnbits.helpers import generate_filter_params_openapi

from .crud import (
    create_pages,
    delete_pages,
    get_pages,
    get_pages_paginated,
    update_pages,
)
from .models import (
    CreatePages,
    Pages,
    PagesFilters,
)

pages_filters = parse_filters(PagesFilters)

custom_public_page_api_router = APIRouter()


############################# Pages #############################
@custom_public_page_api_router.post("/api/v1/pages", status_code=HTTPStatus.CREATED)
async def api_create_pages(
    data: CreatePages,
    user: User = Depends(check_user_exists),
) -> Pages:
    pages = await create_pages(user.id, data)
    return pages


@custom_public_page_api_router.put("/api/v1/pages/{pages_id}", status_code=HTTPStatus.CREATED)
async def api_update_pages(
    pages_id: str,
    data: CreatePages,
    user: User = Depends(check_user_exists),
) -> Pages:
    pages = await get_pages(user.id, pages_id)
    if not pages:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Pages not found.")
    if pages.user_id != user.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this pages.")
    pages = await update_pages(Pages(**{**pages.dict(), **data.dict()}))
    return pages


@custom_public_page_api_router.get(
    "/api/v1/pages/paginated",
    name="Pages List",
    summary="get paginated list of pages",
    response_description="list of pages",
    openapi_extra=generate_filter_params_openapi(PagesFilters),
    response_model=Page[Pages],
)
async def api_get_pages_paginated(
    user: User = Depends(check_user_exists),
    filters: Filters = Depends(pages_filters),
) -> Page[Pages]:

    return await get_pages_paginated(
        user_id=user.id,
        filters=filters,
    )


@custom_public_page_api_router.get(
    "/api/v1/pages/{pages_id}",
    name="Get Pages",
    summary="Get the pages with this id.",
    response_description="An pages or 404 if not found",
    response_model=Pages,
)
async def api_get_pages(
    pages_id: str,
    user: User = Depends(check_user_exists),
) -> Pages:

    pages = await get_pages(user.id, pages_id)
    if not pages:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Pages not found.")

    return pages


@custom_public_page_api_router.delete(
    "/api/v1/pages/{pages_id}",
    name="Delete Pages",
    summary="Delete the pages " "and optionally all its associated client_data.",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_pages(
    pages_id: str,
    clear_client_data: bool | None = False,
    user: User = Depends(check_user_exists),
) -> SimpleStatus:

    await delete_pages(user.id, pages_id)
    if clear_client_data is True:
        # await delete all client data associated with this pages
        pass
    return SimpleStatus(success=True, message="Pages Deleted")
