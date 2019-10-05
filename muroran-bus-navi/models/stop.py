from . import Base, TripSchema

import re
import uuid
from datetime import datetime
import pygeohash as geohash
import mercantile

from sqlalchemy import (
    Column,
    DateTime,
    String,
    Unicode,
    Integer,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.orm import relationship

from marshmallow import Schema, fields

from marshmallow_sqlalchemy import ModelSchema


class StopName(Base):
    __tablename__ = "stop_names"
    id = Column(String(32), primary_key=True)
    stop_code = Column(String(32), ForeignKey("stops.id"), nullable=False)
    code = Column(String(255), index=True)
    name = Column(Unicode(255), nullable=False, index=True)
    desc = Column(Unicode(255), index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)

    def __init__(
        self, stop_code, code, name, desc, application_start, application_end
    ):
        self.id = uuid.uuid4().hex
        self.stop_code = stop_code
        self.code = code
        self.name = name
        self.desc = desc
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def __repr__(self):
        return "<StopName('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'>" % (
            self.id,
            self.stop_code,
            self.code,
            self.name,
            self.desc,
            self.registered_on,
            self.application_start,
            self.application_end,
        )

    def availability(self, t=datetime.utcnow()):
        if self.application_start <= t and (
            self.application_end is None or self.application_end > t
        ):
            return True
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "stop_code": self.stop_code,
            "name": self.name,
            "desc": self.desc,
            "application_start": self.application_start.isoformat(),
            "application_end": self.application_end.isoformat()
            if self.application_end is not None
            else None,
        }


class StopNameSchema(ModelSchema):
    class Meta:
        model = StopName


# class StopNameTranslation(Base):
#     __tablename__ = 'stop_name_translations'
#     id = Column(String(32), primary_key=True)
#     stop_name_code = Column(String(32), ForeignKey('stop_names.id'),
#                             nullable=False)
#     lang = Column(String(12), nullable=False, index=True)
#     translation = Column(Unicode(255), nullable=False, index=True)
#     registered_on = Column(DateTime, nullable=False, index=True)
#     application_start = Column(DateTime, nullable=False, index=True)
#     application_end = Column(DateTime, index=True)
#
#     def __init__(self, stop_code, code, name, desc,
#                  application_start, application_end):
#         self.id = uuid.uuid4().hex
#         self.stop_name_code = stop_name_code
#         self.lang = lang
#         self.translation = translation
#         self.registered_on = datetime.utcnow()
#         self.application_start = application_start
#         self.application_end = application_end
#
#     def __repr__(self):
#         return "<StopNameTranslation('%s', '%s', '%s', '%s', '%s', "\
#                "'%s', '%s'>" % (self.id, self.stop_name_code, self.lang,
#                                 self.translation, self.registered_on,
#                                 self.application_start, self.application_end)
#
#     def availability(self, t=datetime.utcnow()):
#         if self.application_start <= t and (
#                self.application_end == None or self.application_end > t
#         ):
#             return True
#         return False


class StopPosition(Base):
    __tablename__ = "stop_positions"
    id = Column(String(32), primary_key=True)
    stop_code = Column(String(32), ForeignKey("stops.id"), nullable=False)
    stop_id_prefix = Column(String(255), index=True)
    stop_id = Column(String(255), index=True)
    code = Column(String(255), index=True)
    subname = Column(Unicode(255), index=True)
    desc = Column(Unicode(255), index=True)
    #    latlng = GeometryColumn(POINT(srid=4326), nullable=False, index=True)
    lat = Column(DECIMAL(9, 7), nullable=False, index=True)
    lng = Column(DECIMAL(10, 7), nullable=False, index=True)
    geohash = Column(String(255), nullable=False, index=True)
    quadkey = Column(String(255), nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)

    def __init__(
        self,
        stop_code,
        stop_id_prefix,
        stop_id,
        code,
        subname,
        desc,
        lat,
        lng,
        application_start,
        application_end,
    ):
        self.id = uuid.uuid4().hex
        self.stop_code = stop_code
        self.stop_id_prefix = stop_id_prefix
        self.stop_id = stop_id
        self.code = code
        self.subname = subname
        self.desc = desc
        self.lat = lat
        self.lng = lng
        self.geohash = geohash.encode(lat, lng)
        tile = mercantile.tile(lng, lat, 32)
        self.quadkey = mercantile.quadkey(tile.x, tile.y, tile.z)
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def __repr__(self):
        return (
            "<StopPosition('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',"
            " '%s', '%s', '%s', '%s', '%s', '%s'>"
            % (
                self.id,
                self.stop_code,
                self.stop_id_prefix,
                self.stop_id,
                self.code,
                self.subname,
                self.desc,
                self.lat,
                self.lng,
                self.geohash,
                self.quadkey,
                self.registered_on,
                self.application_start,
                self.application_end,
            )
        )

    def availability(self):
        if self.application_start < datetime.utcnow() and (
            self.application_end is None
            or self.application_end > datetime.utcnow()
        ):
            return True
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "stop_code": self.stop_code,
            "subname": self.subname,
            "desc": self.desc,
            "lat": "%s" % self.lat,
            "lng": "%s" % self.lng,
            "geohash": self.geohash,
            "quadkey": self.quadkey,
            "application_start": self.application_start.isoformat(),
            "application_end": self.application_end.isoformat()
            if self.application_end is not None
            else None,
        }


class StopPositionSchema(ModelSchema):
    lat = fields.Decimal(as_string=True)
    lng = fields.Decimal(as_string=True)

    stop = fields.Nested("StopSchema")

    class Meta:
        model = StopPosition
        include_fk = True


class StopUrl(Base):
    __tablename__ = "stop_urls"
    id = Column(String(32), primary_key=True)
    stop_code = Column(String(32), ForeignKey("stops.id"), nullable=False)
    stop_id_prefix = Column(String(255), index=True)
    stop_id = Column(String(255), index=True)
    url = Column(String(255))
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)

    def __init__(
        self,
        stop_code,
        stop_id_prefix,
        stop_id,
        url,
        application_start,
        application_end,
    ):
        self.id = uuid.uuid4().hex
        self.stop_code = stop_code
        self.stop_id_prefix = stop_id_prefix
        self.stop_id = stop_id
        self.url = url
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def to_dict(self):
        return {
            "id": self.id,
            "stop_code": self.stop_code,
            "url": self.url,
            "application_start": self.application_start.isoformat(),
            "application_end": self.application_end.isoformat()
            if self.application_end is not None
            else None,
        }


class StopUrlSchema(ModelSchema):
    class Meta:
        model = StopUrl


class StopTime(Base):
    __tablename__ = "stop_times"
    id = Column(String(32), primary_key=True)
    trip_code = Column(String(32), ForeignKey("trips.id"), nullable=False)
    arrival_time = Column(Integer, nullable=False, index=True)
    departure_time = Column(Integer, nullable=False, index=True)
    tz = Column(String(255), index=True)
    stop_code = Column(
        String(32), ForeignKey("stop_positions.id"), nullable=False
    )
    stop_sequence = Column(Integer, nullable=False, index=True)
    stop_headsign = Column(Unicode(255), index=True)
    pickup_type = Column(
        Integer, server_default="0", nullable=False, index=True
    )
    drop_off_type = Column(
        Integer, server_default="0", nullable=False, index=True
    )
    shape_dist_traveled = Column(String(32), index=True)
    id_prefix = Column(String(255), index=True)
    registered_on = Column(DateTime, nullable=False, index=True)

    position = relationship("StopPosition", backref="stop_time")
    trip = relationship("Trip", backref="stop_time")

    def __init__(
        self,
        trip_code,
        arrival_time,
        departure_time,
        tz,
        stop_code,
        stop_sequence,
        stop_headsign,
        pickup_type,
        drop_off_type,
        shape_dist_traveled,
        id_prefix,
    ):
        self.id = uuid.uuid4().hex
        self.trip_code = trip_code
        if arrival_time.isdigit():
            self.arrival_time = arrival_time
        elif re.match(r"(\d+):(\d+):(\d+)", arrival_time):
            m = re.match(r"(\d+):(\d+):(\d+)", arrival_time)
            time = [i for i in map(int, m.groups())]
            self.arrival_time = time[0] * 3600 + time[1] * 60 + time[2]
        elif re.match(r"(\d+):(\d+)", arrival_time):
            m = re.match(r"(\d+):(\d+)", arrival_time)
            time = [i for i in map(int, m.groups())]
            self.arrival_time = time[0] * 3600 + time[1] * 60
        if departure_time.isdigit():
            self.departure_time = departure_time
        elif re.match(r"(\d+):(\d+):(\d+)", departure_time):
            m = re.match(r"(\d+):(\d+):(\d+)", departure_time)
            time = [i for i in map(int, m.groups())]
            self.departure_time = time[0] * 3600 + time[1] * 60 + time[2]
        elif re.match(r"(\d+):(\d+)", departure_time):
            m = re.match(r"(\d+):(\d+)", departure_time)
            time = [i for i in map(int, m.groups())]
            self.departure_time = time[0] * 3600 + time[1] * 60
        self.tz = tz
        self.id_prefix = id_prefix
        self.stop_code = stop_code
        self.stop_sequence = stop_sequence
        self.stop_headsign = stop_headsign
        self.pickup_type = pickup_type
        self.drop_off_type = drop_off_type
        self.shape_dist_traveled = shape_dist_traveled
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return (
            f"<StopTime('{self.id}', '{self.trip_code}', "
            f"'{self.stop_code}', '{self.stop_sequence}')>"
        )


class StopTimeSchema(ModelSchema):
    trip = fields.Nested(TripSchema)
    position = fields.Nested(StopPositionSchema)

    class Meta:
        model = StopTime
        include_fk = True


class DepartureArrivalSchema(Schema):
    # departure_arrival = TupleField((StopTimeSchema(), StopTimeSchema()))
    # departure_arrival = fields.Nested(StopTimeSchema(many=True))
    departure = fields.Nested(StopTimeSchema())
    arrival = fields.Nested(StopTimeSchema())


class Stop(Base):
    __tablename__ = "stops"
    id = Column(String(32), primary_key=True)
    stop_id_prefix = Column(String(255), index=True)
    stop_id = Column(String(255), index=True)
    wheelchair_boarding = Column(Integer, index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)
    name = relationship(
        "StopName", order_by="desc(StopName.application_start)", backref="stop"
    )
    positions = relationship("StopPosition", backref="stop")
    url = relationship("StopUrl", backref="stop")

    def now_name(self):
        for stopname in self.name:
            if stopname.availability:
                return stopname
        return None

    def __init__(
        self,
        stop_id_prefix,
        stop_id,
        wheelchair_boarding,
        application_start,
        application_end,
    ):
        self.id = uuid.uuid4().hex
        self.stop_id_prefix = stop_id_prefix
        self.stop_id = stop_id
        self.wheelchair_boarding = wheelchair_boarding
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end
        self.now_name = self.now_name()

    def __repr__(self):
        return (
            f"<Stop('{self.id}', "
            f"'{self.stop_id_prefix}', '{self.stop_id}', "
            f"'{self.wheelchair_boarding}', '{self.registered_on}', "
            f"'{self.application_start}', '{self.application_end}', "
            f"'{self.name}', '{self.positions}', '{self.url}'>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "wheelchair_boarding": self.wheelchair_boarding,
            "application_start": self.application_start.isoformat(),
            "application_end": self.application_end.isoformat()
            if self.application_end is not None
            else None,
            "name": list([i.to_dict() for i in self.name]),
            "positions": list([p.to_dict() for p in self.positions]),
            "url": list([i.to_dict() for i in self.url]),
        }


class StopSchema(ModelSchema):
    name = fields.Nested(StopNameSchema, many=True)
    now_name = fields.Nested(StopNameSchema)
    positions = fields.Nested(StopPositionSchema, many=True, exclude=["stop"])

    class Meta:
        model = Stop
        include_fk = True
