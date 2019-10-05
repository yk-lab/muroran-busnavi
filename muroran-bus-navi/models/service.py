from . import Base

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    String,
    ForeignKey,
    Boolean,
    Date,
    SmallInteger,
)

# from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import ModelSchema


class ServiceID(Base):
    __tablename__ = "service_id"
    id = Column(String(32), primary_key=True)
    id_prefix = Column(String(255), index=True)
    service_id = Column(String(255), index=True)
    registered_on = Column(DateTime, nullable=False, index=True)

    def __init__(self, id_prefix, service_id):
        self.id = uuid.uuid4().hex
        self.id_prefix = id_prefix
        self.service_id = service_id
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return (
            f"<ServiceID('{self.id}', "
            f"'{self.id_prefix}', '{self.service_id}', "
            f"'{self.registered_on}')>"
        )


class ServiceIDSchema(ModelSchema):
    class Meta:
        model = ServiceID


class Service(Base):
    __tablename__ = "service"
    id = Column(String(32), primary_key=True)
    service_code = Column(
        String(32), ForeignKey("service_id.id"), nullable=False
    )
    monday = Column(Boolean, nullable=False, index=True)
    tuesday = Column(Boolean, nullable=False, index=True)
    wednesday = Column(Boolean, nullable=False, index=True)
    thursday = Column(Boolean, nullable=False, index=True)
    friday = Column(Boolean, nullable=False, index=True)
    saturday = Column(Boolean, nullable=False, index=True)
    sunday = Column(Boolean, nullable=False, index=True)
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime, nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False, index=True)

    def __init__(
        self,
        service_code,
        monday,
        tuesday,
        wednesday,
        thursday,
        friday,
        saturday,
        sunday,
        start_date,
        end_date,
    ):
        self.id = uuid.uuid4().hex
        self.service_code = service_code
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
        self.start_date = start_date
        self.end_date = end_date
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        service_weekday = "".join(
            [
                "T" if i else "F"
                for i in [
                    self.monday,
                    self.tuesday,
                    self.wednesday,
                    self.thursday,
                    self.friday,
                    self.saturday,
                    self.sunday,
                ]
            ]
        )
        return (
            f"<Service('{self.id}', '{self.service_code}', "
            f"'{service_weekday}', "
            f"'{self.start_date}', '{self.end_date}', "
            f"'{self.registered_on}')>"
        )


class ServiceSchema(ModelSchema):
    class Meta:
        model = Service


class ServiceDate(Base):
    __tablename__ = "service_dates"
    id = Column(String(32), primary_key=True)
    service_code = Column(
        String(32), ForeignKey("service_id.id"), nullable=False
    )
    date = Column(Date, nullable=False, index=True)
    timezone = Column(String(255), nullable=False, index=True)
    exception_type = Column(SmallInteger, nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False, index=True)

    def __init__(self, service_code, date, timezone, exception_type):
        self.id = uuid.uuid4().hex
        self.service_code = service_code
        self.date = date
        self.timezone = timezone
        self.exception_type = exception_type
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return (
            f"<ServiceDate('{self.id}', '{self.service_code}',"
            f" '{self.date}', '{self.timezone}', '{self.exception_type}',"
            f" '{self.registered_on}')>"
        )


class ServiceDateSchema(ModelSchema):
    class Meta:
        model = ServiceDate
