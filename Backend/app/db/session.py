from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

_engine = None
_async_session_maker = None


def get_engine():
    global _engine, _async_session_maker

    if _engine is None:
        if not settings.DATABASE_URL_ASYNC:
            raise RuntimeError("DATABASE_URL_ASYNC is not set")

        _engine = create_async_engine(
            settings.DATABASE_URL_ASYNC,
            echo=settings.DEBUG,
            future=True,
        )

        _async_session_maker = sessionmaker(
            _engine, class_=AsyncSession, expire_on_commit=False
        )

    return _engine, _async_session_maker


async def get_async_session():
    _, async_session_maker = get_engine()
    async with async_session_maker() as session:
        yield session
