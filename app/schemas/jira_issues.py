from typing import List

from pydantic import BaseModel


class IssueMetrics(BaseModel):
    jira_issue_id: int
    ai_commits: int
    non_ai_commits: int
    lines_of_code_ai: int
    lines_of_code_non_ai: int


class ListIssueMetrics(BaseModel):
    results: List[IssueMetrics]
    total_ai_commits: int
    avg_proportion_ai_commits: float
