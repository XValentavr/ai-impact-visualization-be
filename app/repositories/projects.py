from app.models import Project
from app.repositories.base import SQLAlchemyRepository


class ProjectRepository(SQLAlchemyRepository):
    model = Project
