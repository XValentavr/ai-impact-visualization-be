import pytest
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Team
from app.repositories.teams import TeamRepository


@pytest.mark.asyncio
async def test_create(async_session: AsyncSession) -> None:
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session

    repo = TeamRepository(session)

    data = {"name": "Test Team"}

    result = await repo.create(data)

    assert result == 1

    team = (await session.execute(select(Team).filter_by(id=result))).scalar_one()

    assert team.name == "Test Team"


@pytest.mark.asyncio
async def test_list(async_session: AsyncSession) -> None:
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session

    repo = TeamRepository(session)
    data = {"name": "Test Team"}
    data1 = {"name": "Test Team"}
    await repo.create(data)
    await repo.create(data1)

    teams = await repo.list()

    assert len(teams) == 2


@pytest.mark.asyncio
async def test_get_by(async_session: AsyncSession) -> None:
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session

    repo = TeamRepository(session)
    data1 = {"name": "Test Team"}
    await repo.create(data1)

    team = await repo.get_by(name="Test Team")

    assert team.name == "Test Team"


@pytest.mark.asyncio
async def test_update(async_session: AsyncSession) -> None:
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session

    repo = TeamRepository(session)
    data1 = {"name": "Test Team"}
    await repo.create(data1)

    data = {"name": "Updated Team"}
    result = await repo.update(1, data)

    assert result == 1

    team = (await session.execute(select(Team).filter_by(id=1))).scalar_one()

    assert team.name == "Updated Team"


@pytest.mark.asyncio
async def test_delete(async_session: AsyncSession) -> None:
    if hasattr(async_session, "__anext__"):
        session = await async_session.__anext__()
    else:
        session = async_session

    data = {"name": "Updated Team"}

    repo = TeamRepository(session)
    await repo.create(data)

    result = await repo.delete(1)

    assert result is True

    # Try to retrieve the deleted team
    team = (await session.execute(select(Team).filter_by(id=1))).scalar_one_or_none()

    assert team is None
