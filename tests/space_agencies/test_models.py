import copy
import uuid
from datetime import datetime

import pytz
from pydantic import ValidationError

from app.space_agencies import models

data = {
    "name": "My Space Agency",
    "description": "It is a great Space Agency.",
    "website": "",
}


def test_space_agency_base():
    space_agency = models.SpaceAgencyBase(**data)
    assert type(space_agency) == models.SpaceAgencyBase


# ---------------------------------------------------------------------
def test_space_agency_without_created_at():
    space_agency = models.SpaceAgency(**data, id=uuid.uuid4())
    assert type(space_agency) == models.SpaceAgency
    assert space_agency.id != None
    assert type(space_agency.id) == uuid.UUID
    assert space_agency.created_at != None
    assert type(space_agency.created_at) == datetime


def test_space_agency_with_created_at():
    space_agency = models.SpaceAgency(
        **data,
        id=uuid.uuid4(),
        created_at=datetime.now().replace(tzinfo=pytz.UTC)
    )
    assert type(space_agency) == models.SpaceAgency
    assert space_agency.id != None
    assert type(space_agency.id) == uuid.UUID
    assert space_agency.created_at != None
    assert type(space_agency.created_at) == datetime


def test_space_agency_with_created_at_without_tz():
    space_agency = models.SpaceAgency(
        **data, id=uuid.uuid4(), created_at=datetime.now()
    )
    assert type(space_agency) == models.SpaceAgency
    assert space_agency.id != None
    assert type(space_agency.id) == uuid.UUID
    assert space_agency.created_at != None
    assert type(space_agency.created_at) == datetime
