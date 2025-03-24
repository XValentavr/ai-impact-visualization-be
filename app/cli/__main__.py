import asyncio
import sys
from pathlib import Path

from app.cli.add_all import _add_all
from app.cli.add_commits import _add_commits
from app.cli.add_jira_issues import _add_jira_issues
from app.cli.add_repositories import _add_repositories

sys.path.append(str(Path(__file__).parent.parent.parent))

import typer

from app.cli.add_engineers import _add_engineers
from app.cli.add_projects import _add_projects
from app.cli.add_teams import _add_teams

app = typer.Typer()


@app.command()
def add_teams() -> None:
    asyncio.run(_add_teams())


@app.command()
def add_engineers() -> None:
    asyncio.run(_add_engineers())


@app.command()
def add_projects() -> None:
    asyncio.run(_add_projects())


@app.command()
def add_repositories() -> None:
    asyncio.run(_add_repositories())


@app.command()
def add_jira_issues() -> None:
    asyncio.run(_add_jira_issues())


@app.command()
def add_commits() -> None:
    asyncio.run(_add_commits())


@app.command()
def add_all() -> None:
    asyncio.run(_add_all())


if __name__ == "__main__":
    app()
