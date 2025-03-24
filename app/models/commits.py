from datetime import date
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Commit(Base):
    __tablename__ = "commits"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    commit_date: Mapped[date]
    ai_used: Mapped[bool]
    lines_of_code: Mapped[int]

    engineer_id: Mapped[int] = mapped_column(
        ForeignKey("engineers.id", ondelete="CASCADE"), index=True
    )
    jira_issue_id: Mapped[int] = mapped_column(
        ForeignKey("jira_issues.id", ondelete="CASCADE"), index=True
    )
    repo_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE")
    )

    engineer: Mapped["Engineer"] = relationship("Engineer", back_populates="commits")
    jira_issue: Mapped["JiraIssue"] = relationship(
        "JiraIssue", back_populates="commits"
    )
    repository: Mapped["Repository"] = relationship(
        "Repository", back_populates="commits"
    )
