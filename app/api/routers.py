from app.api.health_checks import router as health_check_router
from app.api.jira_issues import router as jira_issues_router
from app.api.projects import router as projects_router
from app.api.teams import router as teams_router

all_routers = [
    health_check_router,
    jira_issues_router,
    projects_router,
    teams_router,
]
