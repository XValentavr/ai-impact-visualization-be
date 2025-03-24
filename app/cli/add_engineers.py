import csv

import typer

from app.config.settings import settings
from app.db.db import async_session_maker
from app.models.engineers import Engineer

ENGINEERS_CSV = settings.server.data_dir_path / "engineers.csv"


async def _add_engineers() -> None:
    with open(ENGINEERS_CSV, "r") as f:
        reader = csv.DictReader(f)

        async with async_session_maker() as session:
            for row in reader:
                row["id"] = int(row["id"])
                engineer = Engineer(**row)
                session.add(engineer)
                typer.secho(f"Added engineer {engineer.name}", fg=typer.colors.GREEN)

            await session.commit()
