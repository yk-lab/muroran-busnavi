from . import Base

from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer
from marshmallow_sqlalchemy import ModelSchema


class UserPermission(Base):
    __tablename__ = "user_permissions"
    id = Column(Integer, primary_key=True)
    uid = Column(String(28), nullable=False, index=True)
    permission = Column(Integer, nullable=False, index=True)
    registered_on = Column(DateTime, nullable=False)
    application_start = Column(DateTime, nullable=False, index=True)

    PERMITTED_COMPANY_ALL = 0x000000F
    PERMITTED_STOP_ALL = 0x00000F0
    PERMITTED_TIMETABLE_ALL = 0x0000F00
    PERMITTED_ROUTE_ALL = 0x000F000
    PERMITTED_TRIP_ALL = 0x00F0000
    PERMITTED_ACCOUNT_ALL = 0x0F00000
    PERMITTED_CONTROL_ALL = 0xF000000

    COMPANY_PERMISSION = 1
    STOP_PERMISSION = 2
    TIMETABLE_PERMISSION = 3
    ROUTE_PERMISSION = 4
    TRIP_PERMISSION = 5
    ACCOUNT_PERMISSION = 6
    CONTROL_PERMISSION = 7

    PERMIT_VIEW = 0b0001
    PERMIT_INSERT = 0b0010
    PERMIT_UPDATE = 0b0100
    PERMIT_REMOVE = 0b1000

    def __init__(self, uid, permission, application_start):
        self.uid = uid
        self.permission = permission
        self.registered_on = datetime.utcnow()
        self.application_start = application_start

    def _shift(self, digit):
        return 4 * (digit - 1)

    def get_permission(self):
        return self.permission

    def permitted_stop_insert(self):
        return (
            True
            if (
                self.get_permission
                & (self.PERMIT_INSERT << self._shift(self.STOP_PERMISSION))
            )
            != 0
            else False
        )

    def permitted_stop_update(self):
        return (
            True
            if (
                self.get_permission
                & (self.PERMIT_UPDATE << self._shift(self.STOP_PERMISSION))
            )
            != 0
            else False
        )


class UserPermissionSchema(ModelSchema):
    class Meta:
        model = UserPermission
