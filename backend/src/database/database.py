from asyncio import current_task
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, as_declarative, declared_attr, mapped_column

from src.config import settings

engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_scoped_session(async_session, scopefunc=current_task)
    try:
        yield session
    finally:
        await session.remove()


@as_declarative()
class Base:
    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
