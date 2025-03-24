from fastapi import APIRouter

from app.db.db import SessionDep
from app.schemas.teams import TeamListSchema
from app.services.teams import TeamService

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("", response_model=TeamListSchema)
async def get_all_teams(session: SessionDep) -> TeamListSchema:
    service = TeamService(session)
    return await service.get_all()
