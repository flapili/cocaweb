# coding: utf-8
import datetime
from typing import Optional, Union, List
from urllib.parse import urlencode

from fastapi import Security, HTTPException, Depends, status
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKeyCookie
from pydantic import PositiveInt
from jose import JWTError, jwt

from modularapi.db import db

from .settings import get_setting, Setting
from .models import UserInDB, MemberInDB

from modules.discord_stats.db import User, Member


def get_Oauth2_url(redirect_uri: str, scopes: List[str]) -> str:
    discord_url = "https://discord.com/oauth2/authorize?"
    return discord_url + urlencode(
        {
            "client_id": get_setting().CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(scopes),
        }
    )


def create_JWT_token(
    data: dict,
    expires_delta: datetime.timedelta,
    secret_key: str,
    algorithm: str,
) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def get_jwt_token(
    jwt_token_query: str = Security(APIKeyQuery(name=get_setting().JWT_TOKEN_NAME, auto_error=False)),
    jwt_token_header: str = Security(APIKeyHeader(name=get_setting().JWT_TOKEN_NAME, auto_error=False)),
    jwt_token_cookie: str = Security(APIKeyCookie(name=get_setting().JWT_TOKEN_NAME, auto_error=False)),
    setting: Setting = Depends(get_setting),
) -> str:
    if jwt_token_query is not None:
        return jwt_token_query

    elif jwt_token_header is not None:
        return jwt_token_header

    elif jwt_token_cookie is not None:
        return jwt_token_cookie

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": f"{setting.JWT_TOKEN_NAME} is missing",
                "login_url": get_Oauth2_url(
                    redirect_uri=f"{setting.WEBSITE_BASE_URL}/api/discord_Oauth2",
                    scopes=["identify", "guilds.join"],
                ),
            },
        )


async def get_current_user(
    guild_id: Optional[PositiveInt],
    jwt_token: str = Depends(get_jwt_token),
    setting: Setting = Depends(get_setting),
) -> Union[UserInDB, MemberInDB]:
    try:
        payload = jwt.decode(jwt_token, setting.JWT_TOKEN.get_secret_value(), algorithms=[setting.JWT_ALGORITHM])
        user_id = int(payload["user_id"])  # te be sure user_id is an id
        if guild_id is None:
            user = await User.get(user_id)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "message": "404 : User not Found",
                        "login_url": get_Oauth2_url(
                            redirect_uri=f"{setting.WEBSITE_BASE_URL}/api/discord_Oauth2",
                            scopes=["identify", "guilds.join"],
                        ),
                    },
                )

            return UserInDB(**user.to_dict())

        member = (
            await db.select(
                [
                    User.id,
                    User.username,
                    User.discriminator,
                    User.avatar,
                    Member.guild_id,
                    Member.display_name,
                    Member.joined_at,
                ]
            )
            .select_from(User.join(Member, Member.user_id == User.id))
            .where(User.id == user_id)
            .where(Member.guild_id == guild_id)
            .gino.one_or_none()
        )
        if member is not None:
            user_id, username, discriminator, avatar, guild_id2, display_name, joined_at = member
            return MemberInDB(
                id=user_id,
                username=username,
                discriminator=discriminator,
                avatar=avatar,
                guild_id=guild_id2,
                display_name=display_name,
                joined_at=joined_at,
            )

        user = await User.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "404 : User not Found",
                    "login_url": get_Oauth2_url(
                        redirect_uri=f"{setting.WEBSITE_BASE_URL}/api/discord_Oauth2",
                        scopes=["identify", "guilds.join"],
                    ),
                },
            )
        return UserInDB(**user.to_dict())

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": f"Could not validate {setting.JWT_TOKEN_NAME}",
                "login_url": get_Oauth2_url(
                    redirect_uri=f"{setting.WEBSITE_BASE_URL}/api/discord_Oauth2",
                    scopes=["identify", "guilds.join"],
                ),
            },
        )
