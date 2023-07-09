import logging
from typing import List
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import and_, delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.space_agencies import dbrel, models

LOGGER = logging.getLogger()


async def create_space_agency(
    db: AsyncSession, space_agency: models.SpaceAgencyBase
):
    async with db.begin():
        db_space_agency = dbrel.SpaceAgency(**space_agency.model_dump())
        db.add(db_space_agency)
    await db.commit()
    await db.refresh(db_space_agency)
    return db_space_agency


async def update_space_agency(
    db: AsyncSession,
    space_agency_id: UUID4,
    space_agency: models.SpaceAgencyBase,
):
    async with db.begin():
        result = await db.execute(
            update(dbrel.SpaceAgency)
            .where(dbrel.SpaceAgency.id == space_agency_id)
            .values(**space_agency.model_dump())
        )
    if result.rowcount > 0:
        return await get_space_agency_by_id(db, space_agency_id)
    return None


async def delete_space_agency(db: AsyncSession, space_agency_id: uuid4):
    async with db.begin():
        result = await db.execute(
            delete(dbrel.SpaceAgency).where(
                dbrel.SpaceAgency.id == space_agency_id
            )
        )
        return result.rowcount


async def count_space_agencies(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(func.count(dbrel.SpaceAgency.id)))
        return result.scalars().one()


async def get_space_agency_by_id(db: AsyncSession, space_agency_id: uuid4):
    async with db.begin():
        result = await db.execute(
            select(dbrel.SpaceAgency).where(
                dbrel.SpaceAgency.id == space_agency_id
            )
        )
        first_result = result.first()
        if first_result is None:
            return None
        (first,) = first_result
        return first


async def list_space_agencies(
    db: AsyncSession, offset: int = 0, limit: int = 10
) -> List[dbrel.SpaceAgency]:
    async with db.begin():
        result = await db.execute(
            select(dbrel.SpaceAgency)
            .offset(offset)
            .limit(limit)
            .order_by(
                dbrel.SpaceAgency.created_at,
            )
        )
        return [item for item, in result.fetchall()]
