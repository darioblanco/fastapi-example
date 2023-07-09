from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

if getenv("ENV") == "test":
    engine = create_async_engine(
        getenv("DATABASE_TEST_URI"), poolclass=NullPool
    )
else:  # pragma: no cover
    engine = create_async_engine(getenv("DATABASE_URI"))

async_session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
        await session.close()
