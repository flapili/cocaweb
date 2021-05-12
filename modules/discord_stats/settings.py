# coding: utf-8
import os
from functools import lru_cache

from pydantic import AnyHttpUrl, HttpUrl, SecretStr

from modularapi.settings import Setting


class MessageSettings(Setting):
    DISCORD_API_BASE_URL: HttpUrl = "https://discord.com/api/v9"
    CLIENT_ID: int
    CLIENT_SECRET: SecretStr
    REDIRECT_URI: AnyHttpUrl
    GUILD_ID: int
    BOT_TOKEN: SecretStr


@lru_cache()
def get_setting() -> MessageSettings:
    return MessageSettings(
        _env_file=os.environ.get("DOTENV_PATH", ".env"),
        _env_file_encoding="utf-8",
    )
