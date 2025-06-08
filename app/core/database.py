from sqlalchemy import create_engine
from contextlib import contextmanager
from typing import Iterator
from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# Synchronous engine and session
engine = create_engine(
    str(settings.database_uri),
    pool_pre_ping=True,
    pool_recycle=3600,
    max_overflow=20,
)


@contextmanager
def get_session(autocommit=False) -> Iterator[Session]:
    session = Session(engine, autoflush=False)
    try:
        yield session
        if autocommit:
            session.commit()
    except Exception:
        session.rollback()
        raise
    else:
        session.close()


# Asynchronous engine and session
ASYNC_DATABASE_URL = str(settings.database_uri).replace(
    "postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    max_overflow=20,
)
AsyncSessionLocal = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
