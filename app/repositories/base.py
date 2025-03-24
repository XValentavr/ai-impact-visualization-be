from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> list:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def update(self, id_: int, data: dict) -> int:
        stmt = (
            update(self.model).values(**data).filter_by(id=id_).returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def list(self) -> list:
        res = await self.session.execute(select(self.model))
        return res.scalars().all()  # noqa

    async def get_by(self, **filter_by: dict) -> Type["model"]:  # noqa
        res = await self.session.execute(select(self.model).filter_by(**filter_by))
        return res.scalar_one()

    async def delete(self, id_: int) -> bool:
        await self.session.execute(delete(self.model).filter_by(id=id_))
        await self.session.commit()
        return True
