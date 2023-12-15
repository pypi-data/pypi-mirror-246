"""
    These are tiktok user's related models.
"""
from typing import Optional
from pydantic.dataclasses import dataclass

from .bases import BaseModel, BaseSingleItemResponse


__all__ = [
    "TiktokUserDetailsResponse",
    "TiktokUserDetailsData",
    "TiktokUserStatsData",
    "TiktokUserExtraData",
    "TiktokUserPlatformsData",
]


@dataclass
class TiktokUserPlatformsData(BaseModel):
    """
    A class representing the tiktok user's platforms data.
    """

    youtube_id: Optional[str]
    ins_id: Optional[str]
    twitter_id: Optional[str]


@dataclass
class TiktokUserExtraData(BaseModel):
    """
    A class representing the tiktok user's extra data.
    """

    is_private_account: Optional[bool]
    is_under_18: Optional[bool]
    is_ad_virtual: Optional[bool]


@dataclass
class TiktokUserStatsData(BaseModel):
    """
    A class representing the tiktok user's stats data.
    """

    digg_count: Optional[int]
    follower_count: int
    following_count: int
    heart: Optional[int]
    heart_count: Optional[int]
    video_count: int


@dataclass
class TiktokUserDetailsData(BaseModel):
    """
    A class representing the tiktok user's details data.
    """

    handle: str
    sec_uid: str
    user_id: int
    avatar_url: str
    signature: str
    region: Optional[str]
    category: Optional[str]
    is_verified: bool
    stats: TiktokUserStatsData
    platforms: TiktokUserPlatformsData
    extra: TiktokUserExtraData


@dataclass
class TiktokUserDetailsResponse(BaseSingleItemResponse):
    """
    A class representing the tiktok user's details response data.
    """

    user: TiktokUserDetailsData
