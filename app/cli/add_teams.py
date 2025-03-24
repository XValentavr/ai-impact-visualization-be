import csv

import typer

from app.config.settings import settings
from app.db.db import async_session_maker
from app.models import Team
from app.models.engineers import Engineer

TEAMS_CSV = settings.server.data_dir_path / "teams.csv"


async def _add_teams() -> None:
    with open(TEAMS_CSV, "r") as f:
        reader = csv.DictReader(f)

        async with async_session_maker() as session:
            for row in reader:
                row["team_id"] = int(row["team_id"])
                team = Team(id=row["team_id"], name=row["team_name"])
                session.add(team)
                typer.secho(f"Added team {team.name}", fg=typer.colors.GREEN)

                engineers_ids = row["engineer_ids"].split(",")
                row["engineer_ids"] = [int(id_) for id_ in engineers_ids]
                for engineer_id in row["engineer_ids"]:
                    engineer = await session.get(Engineer, engineer_id)
                    if engineer is None:
                        typer.secho(
                            f"Engineer with id {engineer_id} not found",
                            fg=typer.colors.RED,
                        )
                        continue

                    engineer.team_id = row["team_id"]
                    session.add(engineer)
                    typer.secho(
                        f"Added engineer {engineer.name} to team {team.name}",
                        fg=typer.colors.GREEN,
                    )

            await session.commit()
