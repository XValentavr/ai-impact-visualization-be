from fastapi import APIRouter

from app.db.db import SessionDep
from app.schemas.projects import ProjectListSchema
from app.services.projects import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=ProjectListSchema)
async def get_all_projects(session: SessionDep) -> ProjectListSchema:
    service = ProjectService(session)
    return await service.get_all()
