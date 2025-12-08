from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import (
    CreatePages,
    Pages,
    PagesFilters,
)

db = Database("ext_custom_public_page")


async def create_pages(user_id: str, data: CreatePages) -> Pages:
    pages = Pages(**data.dict(), id=urlsafe_short_hash(), user_id=user_id)
    await db.insert("custom_public_page.pages", pages)
    return pages


async def get_pages(
    user_id: str,
    pages_id: str,
) -> Pages | None:
    return await db.fetchone(
        """
            SELECT * FROM custom_public_page.pages
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": pages_id, "user_id": user_id},
        Pages,
    )


async def get_pages_by_id(
    pages_id: str,
) -> Pages | None:
    return await db.fetchone(
        """
            SELECT * FROM custom_public_page.pages
            WHERE id = :id
        """,
        {"id": pages_id},
        Pages,
    )


async def get_pages_ids_by_user(
    user_id: str,
) -> list[str]:
    rows: list[dict] = await db.fetchall(
        """
            SELECT DISTINCT id FROM custom_public_page.pages
            WHERE user_id = :user_id
        """,
        {"user_id": user_id},
    )

    return [row["id"] for row in rows]


async def get_pages_paginated(
    user_id: str | None = None,
    filters: Filters[PagesFilters] | None = None,
) -> Page[Pages]:
    where = []
    values = {}
    if user_id:
        where.append("user_id = :user_id")
        values["user_id"] = user_id

    return await db.fetch_page(
        "SELECT * FROM custom_public_page.pages",
        where=where,
        values=values,
        filters=filters,
        model=Pages,
    )


async def update_pages(data: Pages) -> Pages:
    await db.update("custom_public_page.pages", data)
    return data


async def delete_pages(user_id: str, pages_id: str) -> None:
    await db.execute(
        """
            DELETE FROM custom_public_page.pages
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": pages_id, "user_id": user_id},
    )
