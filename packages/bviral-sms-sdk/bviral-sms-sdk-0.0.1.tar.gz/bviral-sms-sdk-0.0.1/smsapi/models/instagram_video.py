"""
    These are instagram user's related models.
"""
from typing import List, Optional
from pydantic.dataclasses import dataclass

from .bases import BaseModel, BaseMultiItemsResponse, BaseSingleItemResponse


__all__ = [
    "InstagramVideoDetailsResponse",
    "InstagramVideosResponse",
    "InstagramVideoStatsData",
    "InstagramVideoAuthorData",
    "InstagramVideoDetailsData",
]


@dataclass
class InstagramVideoStatsData(BaseModel):
    """
    A class representing the instagram video's stats data.
    """

    like_count: int
    play_count: int
    view_count: Optional[int]
    comment_count: int
    share_count: Optional[int]


@dataclass
class InstagramVideoAuthorData(BaseModel):
    """
    A class representing the instagram video's author data.
    """

    user_id: int
    handle: str
    full_name: str
    avatar_url: str
    is_verified: bool
    is_private: bool


@dataclass
class InstagramVideoDetailsData(BaseModel):
    """
    A class representing the instagram video's details data.

    """

    video_id: int
    code: str
    create_time: int
    duration: float
    play_url: str
    origin_cover: str
    desc: str
    stats: InstagramVideoStatsData
    author: InstagramVideoAuthorData


@dataclass
class InstagramVideoDetailsResponse(BaseSingleItemResponse):
    """
    A class representing the instagram video's details response data.
    """

    video: InstagramVideoDetailsData


@dataclass
class InstagramVideosResponse(BaseMultiItemsResponse):
    """
    A class representing the instagram videos response data.
    """

    videos: List[InstagramVideoDetailsData]
