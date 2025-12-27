import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_async_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

os.environ["ENV"] = "test"
os.environ["DATABASE_URL_ASYNC"] = TEST_DATABASE_URL
os.environ["DATABASE_URL_SYNC"] = "sqlite:///./test.db"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    future=True,
    echo=False,
)

AsyncSessionTest = async_sessionmaker(
    engine_test,
    expire_on_commit=False,
)

async def override_get_async_session():
    async with AsyncSessionTest() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
 transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

@pytest_asyncio.fixture
async def auth_token(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "sadiq",
            "password": "sadiq1234"
        },
    )

    res = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "sadiq1234"
        },
    )

    if res.status_code != 200:
        print(f"Auth failed: {res.text}")

    assert "access_token" in res.json()
    return res.json()["access_token"]
