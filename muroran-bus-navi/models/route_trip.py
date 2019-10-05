from . import Base

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship

from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class Route(Base):
    __tablename__ = "routes"
    id = Column(String(32), primary_key=True)
    agency_code = Column(
        String(32), ForeignKey("companies.id"), nullable=False
    )
    route_short_name = Column(Unicode(255), index=True)
    route_long_name = Column(Unicode(255), index=True)
    route_desc = Column(Unicode(255), index=True)
    route_type = Column(Integer, nullable=False, index=True)
    route_url = Column(Unicode(255))
    route_color = Column(Unicode(255))
    route_text_color = Column(Unicode(255))
    id_prefix = Column(String(255), index=True)
    route_id = Column(String(255), index=True)
    registered_on = Column(DateTime, nullable=False, index=True)

    def __init__(
        self,
        agency_code,
        route_short_name,
        route_long_name,
        route_desc,
        route_type,
        route_url,
        route_color,
        route_text_color,
        id_prefix,
        route_id,
    ):
        self.id = uuid.uuid4().hex
        self.agency_code = agency_code
        self.route_short_name = agency_code
        self.route_long_name = route_long_name
        self.route_desc = route_desc
        self.route_type = route_type
        self.route_url = route_url
        self.route_color = route_color
        self.route_text_color = route_text_color
        self.id_prefix = id_prefix
        self.route_id = route_id
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return (
            f"<Route('{self.id}', '{self.agency_code}', "
            f"'{self.route_short_name}', '{self.route_long_name}', "
            f"'{self.route_desc}', '{self.route_type}', "
            f"'{self.route_url}', "
            f"'{self.route_color}', '{self.route_text_color}', "
            f"'{self.id_prefix}', '{self.route_id}', "
            f"'{self.registered_on}')>"
        )


class RouteSchema(ModelSchema):
    class Meta:
        model = Route


class Trip(Base):
    __tablename__ = "trips"
    id = Column(String(32), primary_key=True)
    route_code = Column(String(32), ForeignKey("routes.id"), nullable=False)
    service_code = Column(
        String(32), ForeignKey("service_id.id"), nullable=False
    )
    trip_headsign = Column(Unicode(255), index=True)
    trip_short_name = Column(Unicode(255), index=True)
    direction_id = Column(String(255), index=True)
    block_id = Column(String(32), index=True)
    shape_code = Column(String(32), index=True)
    id_prefix = Column(String(255), index=True)
    trip_id = Column(String(255), index=True)
    registered_on = Column(DateTime, nullable=False, index=True)

    route = relationship("Route", backref="trip")

    def __init__(
        self,
        route_code,
        service_code,
        trip_headsign,
        trip_short_name,
        direction_id,
        block_id,
        shape_code,
        id_prefix,
        trip_id,
    ):
        self.id = uuid.uuid4().hex
        self.route_code = route_code
        self.service_code = service_code
        self.trip_headsign = trip_headsign
        self.trip_short_name = trip_short_name
        self.direction_id = direction_id
        self.block_id = block_id
        self.shape_code = shape_code
        self.id_prefix = id_prefix
        self.trip_id = trip_id
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return f"<Trip('{self.id}')>"


class TripSchema(ModelSchema):
    route = fields.Nested(RouteSchema)

    class Meta:
        model = Trip
        include_fk = True
