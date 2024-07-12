from pathlib import Path

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from mixer.backend.sqlalchemy import Mixer
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.db import Base, get_async_session
from app.main import app

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

pytest_plugins = [
    'fixtures.data',
]

TEST_DB = BASE_DIR / 'test.db'
TEST_DATABASE_URL = f'sqlite+aiosqlite:///{str(TEST_DB)}'

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={'check_same_thread': False},
)

TestingSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine,
)


async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def test_client():
    app.dependency_overrides[get_async_session] = override_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mixer():
    mixer_engine = create_engine(f'sqlite:///{str(TEST_DB)}')
    session = sessionmaker(bind=mixer_engine)
    return Mixer(session=session(), commit=True)
