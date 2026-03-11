async def m001_pages(db):
    """
    Initial pages table.
    """

    await db.execute(
        f"""
        CREATE TABLE custom_public_page.pages (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )


async def m002_add_center(db):
    """
    Add center flag to pages.
    """

    await db.execute(
        """
        ALTER TABLE custom_public_page.pages
        ADD COLUMN center BOOLEAN NOT NULL DEFAULT FALSE;
    """
    )
