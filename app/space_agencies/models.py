from datetime import datetime

import pytz
from pydantic import UUID4, BaseModel, validator

from app.validators import get_validator, not_empty


class SpaceAgencyBase(BaseModel):
    name: str
    description: str
    website: str

    _name_not_empty = get_validator("name", val_func=not_empty)


class SpaceAgency(SpaceAgencyBase):
    id: UUID4
    created_at: datetime = None

    @validator("created_at", pre=True, always=True)
    def set_created_at(cls, value):
        if not value:
            return datetime.now().replace(tzinfo=pytz.UTC)
        if value.tzinfo:
            return value
        return value.replace(tzinfo=pytz.UTC)

    class Config:
        orm_mode = True
