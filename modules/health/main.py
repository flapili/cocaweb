# coding: utf-8
from pathlib import Path

from fastapi import FastAPI, APIRouter

from modularapi.db import db

from .models import GetHealthResponse


def on_load(app: FastAPI):
    module_name = Path(__file__).parent.parts[-1]
    router = APIRouter(prefix=f"/api/{module_name}", tags=[module_name])

    @router.get("", response_model=GetHealthResponse)
    async def get():
        return {"health": await db.scalar("SELECT 1") == 1}

    app.include_router(router)
