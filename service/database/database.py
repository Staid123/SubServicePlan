from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncEngine, async_sessionmaker, AsyncSession)
from config import SQLALCHEMY_DATABASE_URL


engine: AsyncEngine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL,
    echo=False,
    echo_pool=False,
    pool_size=5,
    max_overflow=10
)

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

async def session_getter() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

 