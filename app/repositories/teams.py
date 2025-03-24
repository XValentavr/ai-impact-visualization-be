from app.models import Team
from app.repositories.base import SQLAlchemyRepository


class TeamRepository(SQLAlchemyRepository):
    model = Team
