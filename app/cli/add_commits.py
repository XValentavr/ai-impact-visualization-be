import csv
from datetime import datetime
from uuid import UUID

import typer

from app.config.settings import settings
from app.db.db import async_session_maker
from app.models import Commit

COMMITS_CSV = settings.server.data_dir_path / "commits.csv"

CHUNK_SIZE = 10_000


async def _add_commits() -> None:
    """
    Inserts commits from a large CSV file in bulk.
    Expects columns: commit_id, engineer_id, jira_issue_id, repo_id, commit_date,
                     ai_used, lines_of_code
    """
    commits_buffer = []

    async with async_session_maker() as session:
        with open(COMMITS_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                commit_id = UUID(row["commit_id"])
                engineer_id = int(row["engineer_id"])
                jira_issue_id = int(row["jira_issue_id"])
                repo_id = int(row["repo_id"])
                commit_date = datetime.strptime(row["commit_date"], "%Y-%m-%d").date()
                ai_used = row["ai_used"] == "True"
                lines_of_code = int(row["lines_of_code"])

                # Create the Commit object using FKs by ID, not by fetching the object
                commit_obj = Commit(
                    id=commit_id,
                    engineer_id=engineer_id,
                    jira_issue_id=jira_issue_id,
                    repo_id=repo_id,
                    commit_date=commit_date,
                    ai_used=ai_used,
                    lines_of_code=lines_of_code,
                )

                commits_buffer.append(commit_obj)

                # If buffer reached chunk size, bulk insert and clear
                if len(commits_buffer) >= CHUNK_SIZE:
                    session.add_all(commits_buffer)
                    await session.commit()
                    commits_buffer.clear()
                    typer.secho(f"Inserted {idx} commits", fg=typer.colors.GREEN)

            # Insert any leftover rows in final partial chunk
            if commits_buffer:
                session.add_all(commits_buffer)
                await session.commit()

    typer.secho(f"Inserted all commits", fg=typer.colors.GREEN)
