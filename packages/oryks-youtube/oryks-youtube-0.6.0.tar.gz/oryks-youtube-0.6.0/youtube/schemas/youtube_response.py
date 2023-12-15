from typing import Optional

from pydantic import BaseModel, Field

from ..models.resource import Resource
from .page_info import PageInfo


class YouTubeResponse(BaseModel):
    kind: str
    etag: str
    pageInfo: PageInfo
    items: list[Resource] = Field(default_factory=list)
    nextPageToken: Optional[str] = ''
    prevPageToken: Optional[str] = ''
