from sqlalchemy import case, func, select

from app.models import Commit, Engineer, JiraIssue, Repository, Team
from app.repositories.base import SQLAlchemyRepository


class JiraIssueRepository(SQLAlchemyRepository):
    model = JiraIssue

    async def get_issues_stats_by_project(
        self, project_id: int | None, team_id: int | None, engineer_id: int | None
    ) -> list:
        commit_stats_query = select(
            Commit.jira_issue_id,
            func.count(Commit.id).label("total_commits"),
            func.sum(case((Commit.ai_used, 1), else_=0)).label("ai_commits"),
            func.sum(case((Commit.ai_used, Commit.lines_of_code), else_=0)).label(
                "ai_loc"
            ),
            func.sum(case((~Commit.ai_used, Commit.lines_of_code), else_=0)).label(
                "no_ai_loc"
            ),
        )

        if project_id is not None:
            commit_stats_query = commit_stats_query.join(
                Repository, Commit.repo_id == Repository.id
            ).filter(Repository.project_id == project_id)

        if team_id is not None:
            commit_stats_query = (
                commit_stats_query.join(Engineer, Commit.engineer_id == Engineer.id)
                .join(Team, Engineer.team_id == Team.id)
                .filter(Team.id == team_id)
            )

        if engineer_id is not None:
            commit_stats_query = commit_stats_query.filter(
                Commit.engineer_id == engineer_id
            )

        commit_stats = commit_stats_query.group_by(Commit.jira_issue_id).subquery()

        stmt = select(
            JiraIssue.id,
            commit_stats.c.total_commits,
            commit_stats.c.ai_commits,
            commit_stats.c.ai_loc,
            commit_stats.c.no_ai_loc,
        ).join(commit_stats, JiraIssue.id == commit_stats.c.jira_issue_id)

        result = await self.session.execute(stmt)
        return result.all()
