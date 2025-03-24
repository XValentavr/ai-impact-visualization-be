from app.db.db import SessionDep
from app.repositories.teams import TeamRepository
from app.schemas.teams import TeamListSchema, TeamSchema


class TeamService:
    def __init__(self, session: SessionDep) -> None:
        self.repo = TeamRepository(session)

    async def get_all(self) -> TeamListSchema:
        rows = await self.repo.list()
        projects = [TeamSchema(id=row.id, name=row.name) for row in rows]
        return TeamListSchema(results=projects)
