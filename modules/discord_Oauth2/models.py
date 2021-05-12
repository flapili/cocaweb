# coding: utf-8
import datetime
from typing import Optional

from pydantic import BaseModel


class UserInDB(BaseModel):
    id: str
    username: str
    discriminator: str
    avatar: Optional[str]


class MemberInDB(UserInDB):
    guild_id: str
    display_name: Optional[str]
    joined_at: datetime.datetime
