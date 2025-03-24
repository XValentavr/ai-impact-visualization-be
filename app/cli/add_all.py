async def _add_all():
    from app.cli.add_commits import _add_commits
    from app.cli.add_engineers import _add_engineers
    from app.cli.add_jira_issues import _add_jira_issues
    from app.cli.add_projects import _add_projects
    from app.cli.add_repositories import _add_repositories
    from app.cli.add_teams import _add_teams

    await _add_engineers()
    await _add_teams()
    await _add_projects()
    await _add_repositories()
    await _add_jira_issues()
    await _add_commits()
