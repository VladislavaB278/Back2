from abc import ABC, abstractmethod

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import Base


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, no_error=False, raw=False, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def find(self, **filter_by):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: type[Base] | None = None
    no_data_error = HTTPException(
        status_code=404,
        detail="Invalid request, no such data exists.",
    )

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        res = self.model(**data)
        self.session.add(res)
        await self.session.commit()

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        res = [row.to_read_model() for row in res]
        return res

    async def find_one(self, no_error=False, raw=False, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.first()

        if no_error:
            return res

        if not res:
            raise self.no_data_error

        if raw:
            return res[0]

        res = res[0].to_read_model()
        return res

    async def find(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        res = [row.to_read_model() for row in res]
        return res

    async def delete_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.first()
        if not res:
            raise self.no_data_error
        await self.session.delete(res[0])
        await self.session.commit()
