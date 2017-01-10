from bottle import request
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, String, Unicode, Integer, BigInteger, Float, DECIMAL, ForeignKey, func, or_, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import pygeohash as geohash
import mercantile

Base = declarative_base()

def db_init(app):
    engine = create_engine(
        app.config['DB.URL'],
        pool_recycle=5, # 5sec
        echo=app.config['DB.ECHO']
    )
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    app.install(
        sqlalchemy.Plugin(
            engine,
            Base.metadata,
            create=True
        )
    )

class Company(Base):
    __tablename__ = 'companies'
    id = Column(String(32), primary_key=True)
    code = Column(BigInteger)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)
    name = relationship("CompanyName", backref="company_names")
    address = relationship("CompanyAddress", backref="company_addresses")

    def __init__(self, code, application_start, application_end):
        self.id = uuid.uuid4().hex
        self.code = code
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def __repr__(self):
        return "<Company('%s', '%d', '%s', '%s')>" % (self.id, self.code, self.name, self.address)

class CompanyName(Base):
    __tablename__ = 'company_names'
    id = Column(Integer, primary_key=True)
    company_id = Column(String(32), ForeignKey('companies.id'), nullable=False)
    name = Column(Unicode(255), nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)

    def __init__(self, company_id, name, application_start, application_end):
        self.company_id = company_id
        self.name = name
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def __repr__(self):
        return "<CompanyName('%d', '%s', '%s', '%s', '%s')>" % (self.id, self.company_id, self.name, self.registered_on, self.application_start)

class CompanyAddress(Base):
    __tablename__ = 'company_addresses'
    id = Column(Integer, primary_key=True)
    company_id = Column(String(32), ForeignKey('companies.id'), nullable=False)
    region = Column(Unicode(255), nullable=False, index=True)
    city = Column(Unicode(255), nullable=False, index=True)
    address = Column(Unicode(255), nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)

    def __init__(self, company_id, region, city, address, application_start, application_end):
        self.company_id = company_id
        self.region = region
        self.city = city
        self.address = address
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def __repr__(self):
        return "<CompanyName('%d', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.company_id, self.region, self.city, self.address, self.registered_on, self.application_start)


class Stop(Base):
    __tablename__ = 'stops'
    id = Column(String(32), primary_key=True)
    stop_id_prefix = Column(String(255), index=True)
    stop_id = Column(String(255), index=True)
    wheelchair_boarding = Column(Integer, index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)
    name = relationship("StopName",
            # primaryjoin="and_(Stop.id == StopName.stop_code, StopName.application_start < now(), or_(StopName.application_end != None, StopName.application_end > now()))",
#             primaryjoin="and_(Stop.id == StopName.stop_code, StopName.application_start <= '%s')" % datetime.utcnow().isoformat(),
#            primaryjoin="and_(Stop.id == StopName.stop_code, StopName.application_start <= '%s')" % datetime.utcnow().isoformat(),
            order_by=desc("stop_names.application_start"),
#            uselist=False,
            backref="stop")
    positions = relationship("StopPosition", backref="stop")
    url = relationship("StopUrl", backref="stop")

    def __init__(self, stop_id_prefix, stop_id, wheelchair_boarding, application_start, application_end):
        self.id = uuid.uuid4().hex
        self.stop_id_prefix = stop_id_prefix
        self.stop_id = stop_id
        self.wheelchair_boarding = wheelchair_boarding
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end
        self.now_name = None

    def now_name(self):
        for stopname in self.name:
            if stopname.availability:
                return stopname
        return None


    def __repr__(self):
        return "<Stop('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'>" % (self.id, self.stop_id_prefix, self.stop_id, self.wheelchair_boarding, self.registered_on, self.application_start, self.application_end, self.name, self.positions, self.url)

    def to_dict(self):
        return {
            "id": self.id,
            "wheelchair_boarding": self.wheelchair_boarding,
            "application_start": self.application_start.isoformat() if self.application_start != None else None,
            "application_end": self.application_end.isoformat() if self.application_end != None else None,
            "name": list([i.to_dict() for i in self.name]),
            "positions": list([position.to_dict() for position in self.positions]),
            "url": list([i.to_dict() for i in self.url]),
        }

class StopName(Base):
    __tablename__ = 'stop_names'
    id = Column(String(32), primary_key=True)
    stop_code = Column(String(32), ForeignKey('stops.id'), nullable=False)
    code = Column(String(255), index=True)
    name = Column(Unicode(255), nullable=False, index=True)
    desc = Column(Unicode(255), index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)

    def __init__(self, stop_code, code, name, desc, application_start, application_end):
        self.id = uuid.uuid4().hex
        self.stop_code = stop_code
        self.code = code
        self.name = name
        self.desc = desc
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def __repr__(self):
        return "<StopName('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'>" % (self.id, self.stop_code, self.code, self.name, self.desc, self.registered_on, self.application_start, self.application_end)

    def availability(self):
        if self.application_start < datetime.utcnow() and (self.application_end == None or self.application_end > datetime.utcnow()):
            return True
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "stop_code": self.stop_code,
            "name": self.name,
            "desc": self.desc,
            "application_start": self.application_start.isoformat() if self.application_start != None else None,
            "application_end": self.application_end.isoformat() if self.application_end != None else None,
        }

class StopPosition(Base):
    __tablename__ = 'stop_positions'
    id = Column(String(32), primary_key=True)
    stop_code = Column(String(32), ForeignKey('stops.id'), nullable=False)
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

    def __init__(self, stop_code, stop_id_prefix, stop_id, code, subname, desc, lat, lng, application_start, application_end):
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
        return "<StopPosition('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'>" % (self.id, self.stop_code, self.stop_id_prefix, self.stop_id, self.code, self.subname, self.desc, self.lat, self.lng, self.geohash, self.quadkey, self.registered_on, self.application_start, self.application_end)

    def availability(self):
        if self.application_start < datetime.utcnow() and (self.application_end == None or self.application_end > datetime.utcnow()):
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
            "application_start": self.application_start.isoformat() if self.application_start != None else None,
            "application_end": self.application_end.isoformat() if self.application_end != None else None,
        }

class StopUrl(Base):
    __tablename__ = 'stop_urls'
    id = Column(String(32), primary_key=True)
    stop_code = Column(String(32), ForeignKey('stops.id'), nullable=False)
    stop_id_prefix = Column(String(255), index=True)
    stop_id = Column(String(255), index=True)
    url = Column(String(255))
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)

    def __init__(self, stop_code, stop_id_prefix, stop_id, url, application_start, application_end):
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
            "application_start": self.application_start.isoformat() if self.application_start != None else None,
            "application_end": self.application_end.isoformat() if self.application_end != None else None,
        }

class UserPermission(Base):
    __tablename__ = 'user_permissions'
    id = Column(Integer, primary_key=True)
    uid = Column(String(28), nullable=False, index=True)
    permission = Column(Integer, nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)

    PERMITTED_COMPANY_ALL   = 0x000000F
    PERMITTED_STOP_ALL      = 0x00000F0
    PERMITTED_TIMETABLE_ALL = 0x0000F00
    PERMITTED_ROUTE_ALL     = 0x000F000
    PERMITTED_TRIP_ALL      = 0x00F0000
    PERMITTED_ACCOUNT_ALL   = 0x0F00000
    PERMITTED_CONTROL_ALL   = 0xF000000

    COMPANY_PERMISSION   = 1;
    STOP_PERMISSION      = 2;
    TIMETABLE_PERMISSION = 3;
    ROUTE_PERMISSION     = 4;
    TRIP_PERMISSION      = 5;
    ACCOUNT_PERMISSION   = 6;
    CONTROL_PERMISSION   = 7;

    PERMIT_VIEW   = 0b0001
    PERMIT_INSERT = 0b0010
    PERMIT_UPDATE = 0b0100
    PERMIT_REMOVE = 0b1000

    def __init__(self, uid, permission, application_start):
        self.uid = uid
        self.permission = permission
        self.registered_on = datetime.utcnow()
        self.application_start = application_start

    def _shift(self, digit):
        return 4 * (degit - 1)

    def get_permission(self):
        return self.permission

    def permitted_stop_insert(self):
        return True if (get_permission & (PERMIT_INSERT << _shift(STOP_PERMISSION))) != 0 else False

    def permitted_stop_update(self):
        return True if (get_permission & (PERMIT_UPDATE << _shift(STOP_PERMISSION))) != 0 else False


# c3v1oFM08IdLKQUiBFxoT7pT5BS2

'''
class Route():


class Trip():


class StopTime():
'''
