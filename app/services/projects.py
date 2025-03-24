from app.db.db import SessionDep
from app.repositories.projects import ProjectRepository
from app.schemas.projects import ProjectListSchema, ProjectSchema


class ProjectService:
    def __init__(self, session: SessionDep) -> None:
        self.repo = ProjectRepository(session)

    async def get_all(self) -> ProjectListSchema:
        rows = await self.repo.list()
        projects = [ProjectSchema(id=row.id, name=row.name) for row in rows]
        return ProjectListSchema(results=projects)
