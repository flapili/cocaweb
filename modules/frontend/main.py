# coding: utf-8
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

priority = float("inf")  # load the module at the end


def on_load(app: FastAPI):
    app.mount("/", StaticFiles(directory=Path(__file__).parent / "dist", html=True), name="frontend")
