import csv
from datetime import datetime

import typer

from app.config.settings import settings
from app.db.db import async_session_maker
from app.models import Engineer, JiraIssue, Project
from app.models.jira_issues import Categories

JIRA_ISSUES_CSV = settings.server.data_dir_path / "jira_issues.csv"


async def _add_jira_issues()-> None:
    with open(JIRA_ISSUES_CSV, "r") as f:
        reader = csv.DictReader(f)

        async with async_session_maker() as session:
            for row in reader:
                issue_id = int(row["issue_id"])
                project_id = int(row["project_id"])
                author_id = int(row["author_id"])
                category = row["category"].replace(" ", "_").upper()
                creation_date = datetime.strptime(
                    row["creation_date"], "%Y-%m-%d"
                ).date()
                resolution_date = datetime.strptime(
                    row["resolution_date"], "%Y-%m-%d"
                ).date()

                project = await session.get(Project, project_id)
                if project is None:
                    typer.secho(
                        f"Project with id {project_id} not found",
                        fg=typer.colors.RED,
                    )
                    continue

                author = await session.get(Engineer, author_id)
                if author is None:
                    typer.secho(
                        f"Engineer with id {author_id} not found",
                        fg=typer.colors.RED,
                    )
                    continue

                if Categories.__members__.get(category) is None:
                    typer.secho(
                        f"Category {category} not found",
                        fg=typer.colors.RED,
                    )
                    continue

                issue = JiraIssue(
                    id=issue_id,
                    project_id=project_id,
                    engineer_id=author_id,
                    category=Categories[category].name,
                    creation_date=creation_date,
                    resolution_date=resolution_date,
                )
                session.add(issue)
                typer.secho(f"Added issue {issue.id}", fg=typer.colors.GREEN)

            await session.commit()
