from app.db.db import SessionDep
from app.repositories.jira_issues import JiraIssueRepository
from app.schemas.jira_issues import IssueMetrics, ListIssueMetrics


class JiraIssueService:
    def __init__(self, session: SessionDep) -> None:
        self.repo = JiraIssueRepository(session)

    async def get_issues_stats_by_project(
        self, project_id: int | None, team_id: int | None, engineer_id: int | None
    ) -> ListIssueMetrics:
        rows = await self.repo.get_issues_stats_by_project(
            project_id=project_id, team_id=team_id, engineer_id=engineer_id
        )

        issue_metrics_list = []
        total_ai_commits = 0
        total_proportion_ai_commits = 0.0
        for (
            issue_id,
            total_commits,
            ai_commits,
            ai_loc,
            no_ai_loc,
        ) in rows:
            non_ai_commits = total_commits - ai_commits
            proportion_ai = ai_commits / total_commits if total_commits else 0.0

            issue_metrics = IssueMetrics(
                jira_issue_id=issue_id,
                ai_commits=ai_commits,
                non_ai_commits=non_ai_commits,
                lines_of_code_ai=ai_loc,
                lines_of_code_non_ai=no_ai_loc,
            )
            issue_metrics_list.append(issue_metrics)
            total_ai_commits += ai_commits
            total_proportion_ai_commits += proportion_ai

        return ListIssueMetrics(
            results=issue_metrics_list,
            total_ai_commits=total_ai_commits,
            avg_proportion_ai_commits=(
                total_proportion_ai_commits / len(rows) * 100 if rows else 0.0
            ),
        )
