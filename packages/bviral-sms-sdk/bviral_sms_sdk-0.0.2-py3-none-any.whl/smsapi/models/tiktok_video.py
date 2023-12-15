"""
    These are tiktok user's related models.
"""
from typing import List, Optional
from pydantic.dataclasses import dataclass

from .bases import BaseModel, BaseMultiItemsResponse, BaseSingleItemResponse


__all__ = [
    "TiktokVideoDetailsResponse",
    "TiktokVideosResponse",
    "TiktokVideoStatsData",
    "TiktokVideoAuthorData",
    "TiktokVideoDetailsData",
    "TiktokVideoMusicData",
]


@dataclass
class TiktokVideoMusicData(BaseModel):
    """
    A class representing the tiktok video's music data.
    """

    id: int
    title: str
    author: str
    duration: int


@dataclass
class TiktokVideoStatsData(BaseModel):
    """
    A class representing the tiktok video's stats data.
    """

    digg_count: int
    play_count: int
    comment_count: int
    share_count: int
    download_count: int


@dataclass
class TiktokVideoAuthorData(BaseModel):
    """
    A class representing the tiktok video's author data.
    """

    sec_uid: Optional[str]
    handle: str
    user_id: int
    nickname: str


@dataclass
class TiktokVideoDetailsData(BaseModel):
    """
    A class representing the tiktok video's details data.

    """

    video_id: int
    create_time: int
    region: Optional[str]
    duration: int
    nw_play: str
    origin_cover: str
    desc: str
    stats: TiktokVideoStatsData
    music_info: TiktokVideoMusicData
    author: TiktokVideoAuthorData


@dataclass
class TiktokVideoDetailsResponse(BaseSingleItemResponse):
    """
    A class representing the tiktok video's details response data.
    """

    video: TiktokVideoDetailsData


@dataclass
class TiktokVideosResponse(BaseMultiItemsResponse):
    """
    A class representing the tiktok videos response data.
    """

    videos: List[TiktokVideoDetailsData]
