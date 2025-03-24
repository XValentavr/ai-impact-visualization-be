import sys
from typing import AsyncGenerator
import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.orm import sessionmaker

from app.models import Base


@pytest.fixture(scope="function")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_session(
    async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    if hasattr(async_engine, "__anext__"):
        engine = await async_engine.__anext__()
    else:
        engine = async_engine
    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        yield session


@pytest.fixture
def mock_session_dep() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_repo() -> MagicMock:
    repo = MagicMock()
    repo.get_issues_stats_by_project = AsyncMock(
        return_value=[
            (1, 10, 4, 100, 200),
            (2, 5, 2, 50, 75),
        ]
    )
    return repo


def setup_mocks():
    mock_settings = MagicMock()
    mock_settings.postgres.url = "sqlite+aiosqlite:///:memory:"
    sys.modules["app.config.settings"] = MagicMock(settings=mock_settings)

    mock_db = MagicMock()
    mock_db.SessionDep = AsyncSession
    sys.modules["app.db.db"] = mock_db


def get_jira_issue_service(mock_session_dep: MagicMock) -> "JiraIssueService":  # noqa
    setup_mocks()
    for mod in ["app.services.jira_issues", "app.db.db"]:
        from app.services.jira_issues import JiraIssueService

        if mod in sys.modules:
            del sys.modules[mod]
    service = JiraIssueService(mock_session_dep)
    return service
