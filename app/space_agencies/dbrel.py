from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Numeric, String
from sqlalchemy_utils import URLType, UUIDType

from app.db import Base


class SpaceAgency(Base):
    __tablename__ = "space_agencies"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    name = Column(String(50))
    description = Column(String(350))
    website = Column(URLType)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
