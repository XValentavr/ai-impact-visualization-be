from typing import List

from pydantic import BaseModel


class ProjectSchema(BaseModel):
    id: int
    name: str


class ProjectListSchema(BaseModel):
    results: List[ProjectSchema] = []
