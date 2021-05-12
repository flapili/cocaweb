# coding: utf-8
import datetime
from typing import List, Optional


from pydantic import BaseModel


class MessageCount(BaseModel):
    user_id: str
    channel_id: str
    count: int


class Guild(BaseModel):
    id: str
    name: str
    icon: str
    owner_id: str


class GetLeaderboardUserChannel(BaseModel):
    name: str
    id: str
    count: int


class GetLeaderboardUser(BaseModel):
    id: str
    username: str
    discriminator: str
    avatar: Optional[str]
    created_at: datetime.datetime
    display_name: Optional[str]
    joined_at: Optional[datetime.datetime]
    channels: List[GetLeaderboardUserChannel]
    total_messages: int


class GetLeaderboardResponse(BaseModel):
    partial_guild: Guild
    users: List[GetLeaderboardUser]


class GetGuildResponseChannel(BaseModel):
    id: str
    nsfw: bool
    name: str


class GetGuildResponse(BaseModel):
    id: str
    name: str
    icon: str
    owner_id: str
    channels: List[GetGuildResponseChannel]
