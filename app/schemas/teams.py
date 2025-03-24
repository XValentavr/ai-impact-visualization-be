from typing import List

from pydantic import BaseModel


class TeamSchema(BaseModel):
    id: int
    name: str


class TeamListSchema(BaseModel):
    results: List[TeamSchema] = []
