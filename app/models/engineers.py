from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Engineer(Base):
    __tablename__ = "engineers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    team_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), index=True
    )

    commits: Mapped[list["Commit"]] = relationship(back_populates="engineer")  # noqa
    jira_issues: Mapped[list["JiraIssue"]] = relationship(back_populates="engineer")  # noqa
    team: Mapped["Team"] = relationship(back_populates="engineers")  # noqa
