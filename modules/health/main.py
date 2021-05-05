from fastapi import FastAPI

from modularapi.db import db


def on_load(app: FastAPI):
    @app.get("/api/health")
    async def get_health():
        return await db.scalar("SELECT 1") == 1
