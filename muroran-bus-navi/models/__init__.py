from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bottle.ext import sqlalchemy

Base = declarative_base()

from .company import (  # noqa
    Company,  # noqa
    CompanyName,  # noqa
    CompanyAddress,  # noqa
    CompanySchema,  # noqa
    CompanyNameSchema,  # noqa
    CompanyAddressSchema,  # noqa
)  # noqa
from .fare import (  # noqa
    FareAttribute,  # noqa
    FareRule,  # noqa
    FareAttributeSchema,  # noqa
    FareRuleSchema,  # noqa
)  # noqa
from .route_trip import Route, Trip, RouteSchema, TripSchema  # noqa
from .service import (  # noqa
    ServiceID,  # noqa
    Service,  # noqa
    ServiceDate,  # noqa
    ServiceIDSchema,  # noqa
    ServiceSchema,  # noqa
    ServiceDateSchema,  # noqa
)  # noqa
from .stop import (  # noqa
    Stop,  # noqa
    StopName,  # noqa
    StopPosition,  # noqa
    StopUrl,  # noqa
    StopTime,  # noqa
    StopSchema,  # noqa
    StopNameSchema,  # noqa
    StopPositionSchema,  # noqa
    StopUrlSchema,  # noqa
    StopTimeSchema,  # noqa
    DepartureArrivalSchema,  # noqa
)  # noqa
from .user import UserPermission, UserPermissionSchema  # noqa


def Page():
    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "Not Defined")
        self.discription = kwargs.get("discription", None)


def db_init(config, app=None):
    engine = create_engine(
        app.config["DB.URL"] if app else config["DB_URL"],
        pool_recycle=5,  # 5sec
        echo=app.config["DB.ECHO"] if app else config["DB_ECHO"],
    )
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    if app:
        app.install(sqlalchemy.Plugin(engine, Base.metadata, create=True))
    else:
        return session
