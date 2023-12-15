"""
    These are instagram user's related models.
"""
from typing import Optional
from pydantic.dataclasses import dataclass

from .bases import BaseModel, BaseSingleItemResponse


__all__ = [
    "InstagramUserStatsData",
    "InstagramUserDetailsData",
    "InstagramUserDetailsResponse",
]


@dataclass
class InstagramUserStatsData(BaseModel):
    """
    A class representing the instagram user's stats data.
    """

    follower_count: int
    following_count: int
    media_count: int


@dataclass
class InstagramUserDetailsData(BaseModel):
    """
    A class representing the instagram user's details data.
    """

    user_id: int
    handle: str
    full_name: str
    avatar_url: str
    biography: str
    category: Optional[str]
    is_verified: bool
    is_private: bool
    fb_id: int
    country: Optional[str]
    date_joined: Optional[str]
    stats: InstagramUserStatsData


@dataclass
class InstagramUserDetailsResponse(BaseSingleItemResponse):
    """
    A class representing the instagram user's details response data.
    """

    user: InstagramUserDetailsData
