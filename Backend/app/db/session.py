from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=False,
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session():
    async with async_session_maker() as session:
        yield session
