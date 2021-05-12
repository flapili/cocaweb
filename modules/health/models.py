# coding: utf-8
from pydantic import BaseModel


class GetHealthResponse(BaseModel):
    health: bool
