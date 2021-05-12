# coding: utf-8
import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, APIRouter, HTTPException, Depends, status

from modularapi.db import db

from .db import Message, User, Member, Guild, GuildTextChannel
from .models import GetLeaderboardResponse, GetGuildResponse
from .utils import datetime_to_id, id_to_datetime


from modules.discord_Oauth2 import utils as discord_Oauth2_utils


def on_load(app: FastAPI):
    module_name = Path(__file__).parent.parts[-1]
    router = APIRouter(
        prefix=f"/api/{module_name}", tags=[module_name], dependencies=[Depends(discord_Oauth2_utils.get_current_user)]
    )

    @router.get("")
    async def get():
        return "TODO"

    # @router.get("/leaderboard")
    @router.get("/leaderboard", response_model=GetLeaderboardResponse)
    async def get_leaderboard(
        guild_id: int,
        after: Optional[datetime.datetime] = None,
        before: Optional[datetime.datetime] = None,
    ):

        guild = await Guild.get(guild_id)
        if guild is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 : Guild not found")

        query = (
            db.select(
                [
                    User.id,
                    User.username,
                    User.discriminator,
                    User.avatar,
                    Member.display_name,
                    Member.joined_at,
                    Message.channel_id,
                    GuildTextChannel.name,
                    db.func.count(Message.id),
                ]
            )
            .select_from(
                Message.join(User, db.and_(User.id == Message.author_id, Message.guild_id == guild_id))
                .join(
                    Member,
                    db.and_(
                        User.id == Member.user_id,
                        Member.guild_id == guild_id,
                    ),
                    isouter=True,
                )
                .join(
                    GuildTextChannel,
                    db.and_(Message.channel_id == GuildTextChannel.id, GuildTextChannel.guild_id == guild_id),
                )
            )
            .group_by(
                User.id,
                User.username,
                User.discriminator,
                User.avatar,
                Member.display_name,
                Member.joined_at,
                Message.channel_id,
                GuildTextChannel.name,
            )
        )

        if after is not None:
            query = query.where(Message.id >= datetime_to_id(after))

        if before is not None:
            query = query.where(Message.id <= datetime_to_id(before))

        users = {}
        async with db.transaction():
            async for (
                user_id,
                user_username,
                user_discriminator,
                user_avatar,
                user_display_name,
                user_joined_at,
                channel_id,
                channel_name,
                count,
            ) in query.gino.iterate():
                users[user_id] = users.get(
                    user_id,
                    {
                        "id": user_id,
                        "username": user_username,
                        "discriminator": user_discriminator,
                        "avatar": user_avatar,
                        "created_at": id_to_datetime(user_id),
                        "display_name": user_display_name,
                        "joined_at": user_joined_at,
                        "channels": [],
                        "total_messages": 0,
                    },
                )
                users[user_id]["channels"].append({"name": channel_name, "id": channel_id, "count": count})
                users[user_id]["total_messages"] += count
        return {"partial_guild": guild.to_dict(), "users": list(users.values())}

    @router.get("/guild", response_model=GetGuildResponse)
    async def get_guild(guild_id: int):
        query = GuildTextChannel.outerjoin(Guild).select().where(Guild.id == guild_id)
        guild = await query.gino.load(Guild.distinct(Guild.id).load(add_channel=GuildTextChannel)).one_or_none()

        if guild is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 : Guild not found")

        d = guild.to_dict()
        d["channels"] = [c.to_dict() for c in guild.channels]
        for c in d["channels"]:
            del c["guild_id"]
        return d

    app.include_router(router)
