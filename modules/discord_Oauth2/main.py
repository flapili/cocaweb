# coding: utf-8
import datetime
from pathlib import Path
from typing import Union


from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse, PlainTextResponse

import aiohttp

from .settings import get_setting, Setting
from .utils import create_JWT_token, get_current_user, get_Oauth2_url
from .models import UserInDB, MemberInDB


def on_load(app: FastAPI):
    module_name = Path(__file__).parent.parts[-1]
    router = APIRouter(prefix=f"/api/{module_name}", tags=[module_name])

    @router.get("")
    async def get(
        code: str,
        setting: Setting = Depends(get_setting),
    ):
        async with aiohttp.ClientSession() as ses:
            async with ses.post(
                f"{setting.DISCORD_API_BASE_URL}/oauth2/token",
                data={
                    "client_id": setting.CLIENT_ID,
                    "client_secret": setting.CLIENT_SECRET.get_secret_value(),
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": setting.REDIRECT_URI,
                },
            ) as r:
                if r.status >= 400:
                    raise HTTPException(status_code=r.status, detail=await r.text())

                res = await r.json()

            try:
                access_token = res["access_token"]
                token_type = res["token_type"]
            except KeyError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": res["error_description"],
                        "login_url": get_Oauth2_url(
                            redirect_uri=f"{setting.WEBSITE_BASE_URL}/api/discord_Oauth2",
                            scopes=["identify", "guilds.join"],
                        ),
                    },
                )

        async with aiohttp.ClientSession(headers={"Authorization": f"{token_type} {access_token}"}) as ses:
            async with ses.get(f"{setting.DISCORD_API_BASE_URL}/users/@me") as r:
                r.raise_for_status()
                user = await r.json()
                user_id = int(user["id"])

        async with aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {setting.BOT_TOKEN.get_secret_value()}",
                "Content-Type": "application/json",
            }
        ) as ses:
            async with ses.put(
                f"{setting.DISCORD_API_BASE_URL}/guilds/{setting.GUILD_ID}/members/{user_id}",
                json={"access_token": access_token},
            ) as r:
                r.raise_for_status()

        jwt_token = create_JWT_token(
            data={"user_id": user_id},
            expires_delta=datetime.timedelta(days=1),
            secret_key=setting.JWT_TOKEN.get_secret_value(),
            algorithm=setting.JWT_ALGORITHM,
        )

        # TODO redirect from the good page with state
        response = RedirectResponse(setting.WEBSITE_BASE_URL)
        response.set_cookie(key=setting.JWT_TOKEN_NAME, value=jwt_token, secure=True, httponly=True)
        return response

    @router.get("/@me", response_model=Union[MemberInDB, UserInDB])
    async def get_me(me: Union[MemberInDB, UserInDB] = Depends(get_current_user)):
        return me

    @router.delete("/disconnect")
    async def delete_disconnect(
        setting: Setting = Depends(get_setting),
    ):
        """
        TODO
        """
        response = PlainTextResponse("disconnected")
        response.delete_cookie(key=setting.JWT_TOKEN_NAME)
        return response

    app.include_router(router)
