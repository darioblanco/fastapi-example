import json
import os

from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app import config
from app.db import Base
from app.space_agencies import crud as space_agencies_crud
from app.space_agencies import dbrel as space_agencies_dbrel

# from app.reviews import crud as reviews_crud
# from app.reviews import dbrel as reviews_dbrel
# from app.reviews.models import ReviewBase

engine = create_async_engine(os.getenv("DATABASE_TEST_URI"), poolclass=NullPool)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_data_fixture(filename: str):
    if filename is None:
        return {}

    with open(filename, mode="r") as file:
        data = json.load(file)

    return data


async def load_db_with_space_agencies(data):
    db = TestingSessionLocal()
    async with db.begin():
        for data_item in data:
            space_agency = space_agencies_dbrel.SpaceAgency(**data_item)
            db.add(space_agency)
    await db.commit()
    await db.close()


@fixture(autouse=True)
async def recreate_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session
        await session.close()


async def load_space_agencies(db_session):
    data = get_data_fixture(config.DATA_FIXTURES_PATH / "space_agencies.json")
    await load_db_with_space_agencies(data)
    space_agencies_count = await space_agencies_crud.count_space_agencies(
        db_session
    )
    assert space_agencies_count == 4
