from pydantic import BaseModel


class VideoCategory(BaseModel):
    video_category_id: str
    title: str
    assignable: bool
