import enum
from datetime import date

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Categories(enum.Enum):
    BUG_FIX = "Bug Fix"
    FEATURE_DEVELOPMENT = "Feature Development"
    DOCUMENTATION = "Documentation"
    CODE_REFACTORING = "Code Refactoring"
    TASK = "Task"


class JiraIssue(Base):
    __tablename__ = "jira_issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    creation_date: Mapped[date]
    resolution_date: Mapped[date]
    category: Mapped[str] = mapped_column(Enum(Categories))

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    engineer_id: Mapped[int] = mapped_column(
        ForeignKey("engineers.id", ondelete="CASCADE")
    )

    commits: Mapped[list["Commit"]] = relationship(back_populates="jira_issue")  # noqa
    engineer: Mapped["Engineer"] = relationship(back_populates="jira_issues")  # noqa
    project: Mapped["Project"] = relationship(back_populates="jira_issues")  # noqa
