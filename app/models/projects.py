from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    jira_issues: Mapped[list["JiraIssue"]] = relationship(back_populates="project")
    repositories: Mapped[list["Repository"]] = relationship(back_populates="project")
