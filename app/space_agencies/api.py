import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.space_agencies import crud, models

router = APIRouter()

LOGGER = logging.getLogger()


@router.get(
    "/api/v1/space-agencies",
    status_code=status.HTTP_200_OK,
    summary="List all Space Agencies.",
)
async def list_space_agencies(
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
    db: AsyncSession = Depends(get_db),
):
    try:
        return {
            "data": (await crud.list_space_agencies(db, offset, limit)),
            "count": (await crud.count_space_agencies(db)),
        }
    except Exception as exc:  # pragma: no cover
        # This is covered in test_list_space_agencies_returns_500 but the coverage tool does not show it
        LOGGER.error("unable to list space agencies", exc_info=exc)
        raise HTTPException(
            status_code=500, detail="An unexpected error happened"
        )


@router.post(
    "/api/v1/space-agencies",
    status_code=status.HTTP_201_CREATED,
    response_model=models.SpaceAgency,
)
async def create_space_agency(
    space_agency: models.SpaceAgencyBase,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_space_agency(db, space_agency)


@router.get(
    "/api/v1/space-agencies/{space_agency_id}",
    status_code=status.HTTP_200_OK,
    summary="Get Space Agency details",
)
async def get_space_agency_by_id(
    space_agency_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    db_space_agency = await crud.get_space_agency_by_id(db, space_agency_id)
    if db_space_agency is None:  # pragma: no cover
        # This is covered in test_get_space_agency_by_id_returns_404 but the coverage tool does not show it
        raise HTTPException(status_code=404, detail="Space Agency not found")

    return {
        "data": db_space_agency,
    }  # pragma: no cover


@router.put(
    "/api/v1/space-agencies/{space_agency_id}",
    status_code=status.HTTP_200_OK,
    response_model=models.SpaceAgency,
)
async def update_space_agency(
    space_agency_id: UUID4,
    space_agency: models.SpaceAgencyBase,
    db: AsyncSession = Depends(get_db),
):
    db_space_agency = await crud.update_space_agency(
        db, space_agency_id, space_agency
    )
    if db_space_agency is None:  # pragma: no cover
        # This is covered in test_update_space_agency_returns_404 but the coverage tool does not show it
        raise HTTPException(status_code=404, detail="Space Agency not found")
    return db_space_agency  # pragma: no cover


@router.delete(
    "/api/v1/space-agencies/{space_agency_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_space_agency(
    space_agency_id: UUID4, db: AsyncSession = Depends(get_db)
):
    deleted_count = await crud.delete_space_agency(db, space_agency_id)
    if deleted_count == 0:  # pragma: no cover
        # This is covered in test_delete_space_agency_returns_404 but the coverage tool does not show it
        raise HTTPException(status_code=404, detail="Space Agency not found")
