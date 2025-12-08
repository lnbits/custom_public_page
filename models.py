from datetime import datetime, timezone

from lnbits.db import FilterModel
from pydantic import BaseModel, Field


########################### Pages ############################
class CreatePages(BaseModel):
    name: str
    content: str
    center: bool = False
    


class Pages(BaseModel):
    id: str
    user_id: str
    name: str
    content: str
    center: bool = False
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PagesFilters(FilterModel):
    __search_fields__ = [
        "name","content",
    ]

    __sort_fields__ = [
        "name",
        "content",
        "center",
        
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None
