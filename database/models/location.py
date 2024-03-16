from __future__ import annotations

from CHRLINE.services.thrift.ttypes import Location as ThriftLocation
from sqlalchemy import Double
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text

from database.engine import Base, Session


class Location(Base):
    query = Session.query_property()

    title = Column(String(255))
    address = Column(Text, nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    phone = Column(String(30))
    category_id = Column(Integer)
    provider = Column(String(255))
    accuracy = Column(String(255))
    altitude_meters = Column(String(255))

    @classmethod
    def from_line_location(cls, tl: ThriftLocation) -> Location:
        location = cls()
        location.title = tl.title
        location.address = tl.address
        location.latitude = tl.latitude
        location.longitude = tl.longitude
        location.phone = tl.phone
        location.category_id = tl.categoryId
        location.provider = tl.provider
        location.accuracy = tl.accuracy
        location.altitude_meters = tl.altitudeMeters
        return location
