from pydantic import BaseModel, Field

from .resource import Resource


class SecondaryReason(BaseModel):
    id: str
    label: str


class VideoAbuseReportReasonSnippet(BaseModel):
    label: str
    secondary_reasons: list[SecondaryReason] = Field(default_factory=list)


class VideoAbuseReportReason(Resource):
    snippet: VideoAbuseReportReasonSnippet
