import pytest
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project
from app.repositories.projects import ProjectRepository


@pytest.mark.asyncio
async def test_create(async_session: AsyncSession) -> None:
    """Test creating a new project in the repository."""
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session
    repo = ProjectRepository(session)

    data = {"name": "Test Project"}

    result = await repo.create(data)

    assert result == 1

    project = (await session.execute(select(Project).filter_by(id=result))).scalar_one()

    assert project.name == "Test Project"


@pytest.mark.asyncio
async def test_update(async_session: AsyncSession) -> None:
    """Test updating an existing project in the repository."""
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session
    repo = ProjectRepository(session)

    data = {"name": "Old Project"}
    project_id = await repo.create(data)

    updated_data = {"name": "Updated Project"}
    updated_id = await repo.update(project_id, updated_data)

    assert updated_id == project_id

    updated_project = (
        await session.execute(select(Project).filter_by(id=project_id))
    ).scalar_one()

    assert updated_project.name == "Updated Project"


@pytest.mark.asyncio
async def test_list(async_session: AsyncSession) -> None:
    """Test listing all projects in the repository."""
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session
    repo = ProjectRepository(session)

    data1 = {"name": "Project 1"}
    data2 = {"name": "Project 2"}
    await repo.create(data1)
    await repo.create(data2)

    projects = await repo.list()

    assert len(projects) == 2
    assert projects[0].name == "Project 1"
    assert projects[1].name == "Project 2"


@pytest.mark.asyncio
async def test_get_by(async_session: AsyncSession) -> None:
    """Test getting a project by a specific field in the repository."""
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session
    repo = ProjectRepository(session)

    data = {"name": "Unique Project"}
    await repo.create(data)

    project = await repo.get_by(name="Unique Project")

    assert project.name == "Unique Project"


@pytest.mark.asyncio
async def test_delete(async_session: AsyncSession) -> None:
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session
    repo = ProjectRepository(session)

    data = {"name": "Project to Delete"}
    project_id = await repo.create(data)

    success = await repo.delete(project_id)

    assert success is True

    with pytest.raises(Exception):
        await repo.get_by(id=project_id)
