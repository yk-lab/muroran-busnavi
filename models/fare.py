from . import Base

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class FareAttribute(Base):
    __tablename__ = "fare_attributes"
    id = Column(String(32), primary_key=True)
    price = Column(Integer, nullable=False)
    currency_type = Column(String(3), nullable=False)
    payment_method = Column(Integer, nullable=False)
    transfers = Column(Integer, nullable=False)
    agency_code = Column(
        String(32), ForeignKey("companies.id"), nullable=False
    )
    transfer_duration = Column(Integer, nullable=True)
    id_prefix = Column(String(255), nullable=False, index=True)
    fare_id = Column(String(255), nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False, index=True)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, nullable=True, index=True)

    def __init__(
        self,
        price,
        currency_type,
        payment_method,
        transfers,
        agency_code,
        transfer_duration,
        id_prefix,
        fare_id,
        application_start,
        application_end=None,
    ):
        self.id = uuid.uuid4().hex
        self.price = price
        self.currency_type = currency_type
        self.payment_method = payment_method
        self.transfers = transfers
        self.agency_code = agency_code
        self.transfer_duration = transfer_duration
        self.id_prefix = id_prefix
        self.fare_id = fare_id
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def __repr__(self):
        return (
            f"<FareAttribute('{self.id}', '{self.price}', "
            f"'{self.currency_type}', '{self.payment_method}', "
            f"'{self.transfers}', '{self.agency_code}',"
            f" '{self.transfer_duration}', "
            f"'{self.id_prefix}', '{self.fare_id}',"
            f" '{self.application_start}', '{self.application_end}',"
            f" '{self.registered_on}')>"
        )


class FareAttributeSchema(ModelSchema):
    class Meta:
        model = FareAttribute


class FareRule(Base):
    __tablename__ = "fare_rules"
    id = Column(String(32), primary_key=True)
    fare_code = Column(
        String(32), ForeignKey("fare_attributes.id"), nullable=False
    )
    route_code = Column(String(32), nullable=True, index=True)
    origin_code = Column(String(32), nullable=True, index=True)
    destination_code = Column(String(32), nullable=True, index=True)
    contains_code = Column(String(32), nullable=True, index=True)
    id_prefix = Column(String(255), nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False, index=True)
    application_start = Column(DateTime, nullable=False, index=True)
    application_end = Column(DateTime, nullable=True, index=True)
    fare_attribute = relationship("FareAttribute", backref="fare_rule")

    def __init__(
        self,
        fare_code,
        route_code,
        origin_code,
        destination_code,
        contains_code,
        id_prefix,
        application_start,
        application_end=None,
    ):
        self.id = uuid.uuid4().hex
        self.fare_code = fare_code
        self.route_code = route_code
        self.origin_code = origin_code
        self.destination_code = destination_code
        self.contains_code = contains_code
        self.id_prefix = id_prefix
        self.registered_on = datetime.utcnow()
        self.application_start = application_start
        self.application_end = application_end

    def __repr__(self):
        return (
            f"<FareRule('{self.id}', '{self.fare_code}',"
            f" '{self.route_code}',"
            f" '{self.origin_code}', '{self.destination_code}',"
            f" '{self.contains_code}',"
            f" '{self.id_prefix}',"
            f" '{self.application_start}', '{self.application_end}',"
            f" '{self.registered_on}')>"
        )


class FareRuleSchema(ModelSchema):
    fare_attribute = fields.Nested(FareAttributeSchema)

    class Meta:
        model = FareRule
        include_fk = True
