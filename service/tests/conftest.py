import logging
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.pool import NullPool
from service.config import SQLALCHEMY_DATABASE_TEST_URL
from database.models import Base
from database import session_getter
from main import app

# DATABASE
engine_test: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_TEST_URL, poolclass=NullPool)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()  # Закрытие сессии после использования

app.dependency_overrides[session_getter] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        logging.info("CREATING DATABASE")
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        logging.info("DELETING DATABASE")
        await conn.run_sync(Base.metadata.drop_all)
    await engine_test.dispose()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        try:
            yield ac
        finally:
            await ac.aclose()  # Закрытие асинхронного клиента после использования