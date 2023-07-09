import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.space_agencies import crud, dbrel, models
from tests.initialize import TestingSessionLocal, load_space_agencies


# ---------------------------------------------------------------------
async def test_get_space_agency_by_id_returns_None(db_session: AsyncSession):
    space_agency = await crud.get_space_agency_by_id(db_session, uuid.uuid4())
    assert space_agency == None


async def test_get_space_agency_by_id_returns_data(db_session: AsyncSession):
    await load_space_agencies(db_session)
    rid = uuid.UUID("a2db7679-1c0d-4e56-916c-fee0a431c1fa")
    space_agency = await crud.get_space_agency_by_id(db_session, rid)
    assert space_agency.id == rid


# ---------------------------------------------------------------------
async def test_list_space_agency_is_empty(db_session: AsyncSession):
    empty_list = await crud.list_space_agencies(db_session)
    assert len(empty_list) == 0


async def test_list_space_agency_returns_data(db_session: AsyncSession):
    list_before = await crud.list_space_agencies(db_session)
    assert len(list_before) == 0
    await load_space_agencies(db_session)
    list_after = await crud.list_space_agencies(db_session)
    assert len(list_after) == 4


async def test_list_space_agency_offset_and_limit(db_session: AsyncSession):
    await load_space_agencies(db_session)
    # Check the list of space agencies in the fixtures/space_agencies.json file,
    # they are added in that order, and listed in that order too.
    # Fetch the first 2 space agencies:
    my_list = await crud.list_space_agencies(db_session, limit=2)
    assert len(my_list) == 2
    assert my_list[0].id == uuid.UUID("a2db7679-1c0d-4e56-916c-fee0a431c1fa")
    assert my_list[1].id == uuid.UUID("3d2bfdab-aca1-4b0c-8f62-4867aad0173f")
    # Offset the list after 2 space agencies and fetch the next 2 items:
    my_list = await crud.list_space_agencies(db_session, offset=2, limit=2)
    assert len(my_list) == 2
    assert my_list[0].id == uuid.UUID("08d21955-51b6-44e5-83d3-adebb66e7ebd")
    assert my_list[1].id == uuid.UUID("4d3fe717-fd2f-44f2-aa8e-8052f261c094")


# ---------------------------------------------------------------------
async def test_count_space_agencies(db_session: AsyncSession):
    await load_space_agencies(db_session)
    my_count = await crud.count_space_agencies(db_session)
    assert my_count == 4


# ---------------------------------------------------------------------
data = {
    "name": "New Space Agency",
    "description": "It is a New Space Agency.",
    "website": "",
}


async def test_create_space_agency(db_session: AsyncSession):
    space_agency = models.SpaceAgencyBase(**data)
    db_space_agency = await crud.create_space_agency(db_session, space_agency)
    assert type(db_space_agency) == dbrel.SpaceAgency


# ---------------------------------------------------------------------
async def test_update_space_agency(db_session: AsyncSession):
    await load_space_agencies(db_session)
    rid = uuid.UUID("3d2bfdab-aca1-4b0c-8f62-4867aad0173f")
    db_space_agency = await crud.get_space_agency_by_id(db_session, rid)
    # There is no transparent way to get a pydantic model out
    # of a ORM SQLAlchemy object. This is a simple way to do it.
    fields = dict(
        [
            (col.name, getattr(db_space_agency, col.name))
            for col in db_space_agency.__table__.c
        ]
    )
    space_agency = models.SpaceAgency(**fields)
    new_description = "Edited description"
    space_agency.description = new_description
    async with TestingSessionLocal() as session:
        db_space_agency = await crud.update_space_agency(
            session, rid, space_agency
        )
        assert db_space_agency.description == new_description


async def test_update_space_agency_returns_None(db_session: AsyncSession):
    rt = models.SpaceAgency(active=True, id=uuid.uuid4(), **data)
    db_rt = await crud.update_space_agency(db_session, rt.id, rt)
    assert db_rt == None


# ---------------------------------------------------------------------
async def test_delete_space_agency(db_session: AsyncSession):
    deleted = await crud.delete_space_agency(db_session, uuid.uuid4())
    assert deleted == 0
    await load_space_agencies(db_session)
    deleted = await crud.delete_space_agency(
        db_session, uuid.UUID("4d3fe717-fd2f-44f2-aa8e-8052f261c094")
    )
    assert deleted == 1
