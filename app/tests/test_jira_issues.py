import pytest
from unittest.mock import AsyncMock

from .conftest import get_jira_issue_service


@pytest.mark.asyncio
async def test_get_issues_stats_by_project_no_filters(
    mock_session_dep: AsyncMock, mock_repo: AsyncMock
) -> None:
    jira_issue_service = get_jira_issue_service(mock_session_dep)
    jira_issue_service.repo = mock_repo

    result = await jira_issue_service.get_issues_stats_by_project(
        project_id=None, team_id=None, engineer_id=None
    )

    assert len(result.results) == 2
    assert result.total_ai_commits == 6
    assert result.avg_proportion_ai_commits == pytest.approx(40.0, rel=1e-2)

    issue1_metrics = next(m for m in result.results if m.jira_issue_id == 1)
    assert issue1_metrics.ai_commits == 4
    assert issue1_metrics.non_ai_commits == 6
    assert issue1_metrics.lines_of_code_ai == 100
    assert issue1_metrics.lines_of_code_non_ai == 200

    issue2_metrics = next(m for m in result.results if m.jira_issue_id == 2)
    assert issue2_metrics.ai_commits == 2
    assert issue2_metrics.non_ai_commits == 3
    assert issue2_metrics.lines_of_code_ai == 50
    assert issue2_metrics.lines_of_code_non_ai == 75


@pytest.mark.asyncio
async def test_get_issues_stats_by_project_with_project_id(
    mock_session_dep: AsyncMock, mock_repo: AsyncMock
) -> None:
    jira_issue_service = get_jira_issue_service(mock_session_dep)
    jira_issue_service.repo = mock_repo

    await jira_issue_service.get_issues_stats_by_project(
        project_id=1, team_id=None, engineer_id=None
    )
    mock_repo.get_issues_stats_by_project.assert_called_once_with(
        project_id=1, team_id=None, engineer_id=None
    )


@pytest.mark.asyncio
async def test_get_issues_stats_by_project_with_engineer_id(
    mock_session_dep: AsyncMock, mock_repo: AsyncMock
) -> None:
    jira_issue_service = get_jira_issue_service(mock_session_dep)
    jira_issue_service.repo = mock_repo

    await jira_issue_service.get_issues_stats_by_project(
        project_id=None, team_id=None, engineer_id=1
    )
    mock_repo.get_issues_stats_by_project.assert_called_once_with(
        project_id=None, team_id=None, engineer_id=1
    )


@pytest.mark.asyncio
async def test_get_issues_stats_by_project_empty_result(
    mock_session_dep: AsyncMock, mock_repo: AsyncMock
) -> None:
    jira_issue_service = get_jira_issue_service(mock_session_dep)
    mock_repo.get_issues_stats_by_project = AsyncMock(return_value=[])
    jira_issue_service.repo = mock_repo

    result = await jira_issue_service.get_issues_stats_by_project(
        project_id=None, team_id=None, engineer_id=999
    )

    assert len(result.results) == 0
    assert result.total_ai_commits == 0
    assert result.avg_proportion_ai_commits == 0.0
