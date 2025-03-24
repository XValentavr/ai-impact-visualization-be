import csv

import typer

from app.config.settings import settings
from app.db.db import async_session_maker
from app.models import Project

PROJECTS_CSV = settings.server.data_dir_path / "projects.csv"


async def _add_projects()-> None:
    with open(PROJECTS_CSV, "r") as f:
        reader = csv.DictReader(f)

        async with async_session_maker() as session:
            for row in reader:
                row["project_id"] = int(row["project_id"])
                project = Project(id=row["project_id"], name=row["project_name"])
                session.add(project)
                typer.secho(f"Added project {project.name}", fg=typer.colors.GREEN)

            await session.commit()
