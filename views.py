# Description: Add your page endpoints here.

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer
from pydantic import BaseModel

from .crud import get_pages_by_id

custom_public_page_generic_router = APIRouter()


class PreviewPayload(BaseModel):
    content: str | None = ""


def custom_public_page_renderer():
    return template_renderer(["custom_public_page/templates"])

@custom_public_page_generic_router.get("/", response_class=HTMLResponse)
async def index(req: Request, user: User = Depends(check_user_exists)):
    return custom_public_page_renderer().TemplateResponse(
        "custom_public_page/index.html", {"request": req, "user": user.json()}
    )


@custom_public_page_generic_router.post("/preview", response_class=HTMLResponse)
async def preview_page(
    req: Request, payload: PreviewPayload, user: User = Depends(check_user_exists)
):
    content = payload.content or ""
    return custom_public_page_renderer().TemplateResponse(
        "custom_public_page/public_page.html",
        {
            "request": req,
            "content": content,
        },
    )


@custom_public_page_generic_router.get("/{pages_id}")
async def pages_public_page(req: Request, pages_id: str):
    pages = await get_pages_by_id(pages_id)
    if not pages:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Pages does not exist.")

    content = pages.content
    center = pages.center if hasattr(pages, "center") else False

    return custom_public_page_renderer().TemplateResponse(
        "custom_public_page/public_page.html",
        {
            "request": req,
            "content": content,
            "center": center,
        },
    )
