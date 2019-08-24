from . import Base

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    String,
    Unicode,
    Integer,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import ModelSchema


class CompanyName(Base):
    __tablename__ = "company_names"
    id = Column(Integer, primary_key=True)
    company_id = Column(String(32), ForeignKey("companies.id"), nullable=False)
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
        return "<CompanyName('%d', '%s', '%s', '%s', '%s')>" % (
            self.id,
            self.company_id,
            self.name,
            self.registered_on,
            self.application_start,
        )


class CompanyNameSchema(ModelSchema):
    class Meta:
        model = CompanyName


class CompanyAddress(Base):
    __tablename__ = "company_addresses"
    id = Column(Integer, primary_key=True)
    company_id = Column(String(32), ForeignKey("companies.id"), nullable=False)
    region = Column(Unicode(255), nullable=False, index=True)
    city = Column(Unicode(255), nullable=False, index=True)
    address = Column(Unicode(255), nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, index=True)

    def __init__(
        self,
        company_id,
        region,
        city,
        address,
        application_start,
        application_end,
    ):
        self.company_id = company_id
        self.region = region
        self.city = city
        self.address = address
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def __repr__(self):
        return "<CompanyName('%d', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
            self.id,
            self.company_id,
            self.region,
            self.city,
            self.address,
            self.registered_on,
            self.application_start,
        )


class CompanyAddressSchema(ModelSchema):
    class Meta:
        model = CompanyAddress


class Company(Base):
    __tablename__ = "companies"
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
        return (
            f"<Company('{self.id}', '{self.code}', "
            f"'{self.name}', '{self.address}')>"
        )


class CompanySchema(ModelSchema):
    class Meta:
        model = Company
