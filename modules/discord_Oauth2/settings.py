# coding: utf-8
import os
from functools import lru_cache

from pydantic import AnyHttpUrl, HttpUrl, SecretStr

from modularapi.settings import Setting


class DiscordOauth2Setting(Setting):
    DISCORD_API_BASE_URL: HttpUrl = "https://discord.com/api/v9"
    WEBSITE_BASE_URL: HttpUrl
    CLIENT_ID: int
    CLIENT_SECRET: SecretStr
    REDIRECT_URI: AnyHttpUrl
    GUILD_ID: int
    BOT_TOKEN: SecretStr
    JWT_TOKEN: SecretStr
    JWT_TOKEN_NAME: str = "jwt_token"
    JWT_ALGORITHM: str = "HS256"


@lru_cache()
def get_setting() -> DiscordOauth2Setting:
    return DiscordOauth2Setting(
        _env_file=os.environ.get("DOTENV_PATH", ".env"),
        _env_file_encoding="utf-8",
    )
