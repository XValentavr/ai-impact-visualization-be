import csv

import typer

from app.config.settings import settings
from app.db.db import async_session_maker
from app.models import Project, Repository

REPOSITORIES_CSV = settings.server.data_dir_path / "repositories.csv"


async def _add_repositories() -> None:
    with open(REPOSITORIES_CSV, "r") as f:
        reader = csv.DictReader(f)

        async with async_session_maker() as session:
            for row in reader:
                project_id = int(row["project_id"])
                project = await session.get(Project, project_id)
                if project is None:
                    typer.secho(
                        f"Project with id {project_id} not found",
                        fg=typer.colors.RED,
                    )
                    continue

                row["repo_id"] = int(row["repo_id"])
                repository = Repository(
                    id=row["repo_id"], name=row["repo_name"], project_id=project_id
                )
                session.add(repository)
                typer.secho(
                    f"Added repository {repository.name}", fg=typer.colors.GREEN
                )

            await session.commit()
