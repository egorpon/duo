from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from services.auth.config import settings


def get_db_engine() -> AsyncEngine:
    return create_async_engine(str(settings.db_dsn))


def get_async_session() -> AsyncSession:
    return AsyncSession(get_db_engine())


@asynccontextmanager
async def get_session_ctx(session: AsyncSession | None = None):
    if session is not None:
        yield session
    else:
        async with get_async_session() as s:
            yield s
