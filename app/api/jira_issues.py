from fastapi import APIRouter

from app.db.db import SessionDep
from app.schemas.jira_issues import ListIssueMetrics
from app.services.jira_issues import JiraIssueService

router = APIRouter(prefix="/jira-issues", tags=["jira-issues"])


@router.get("/stats", response_model=ListIssueMetrics)
async def get_jira_issues_stats(
    session: SessionDep,
    project_id: int | None = None,
    team_id: int | None = None,
    engineer_id: int | None = None,
) -> ListIssueMetrics:
    service = JiraIssueService(session)
    return await service.get_issues_stats_by_project(
        project_id=project_id, team_id=team_id, engineer_id=engineer_id
    )
