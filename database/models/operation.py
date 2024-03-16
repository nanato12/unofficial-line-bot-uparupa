from __future__ import annotations

from CHRLINE.services.thrift.ttypes import Message as ThriftMessage
from CHRLINE.services.thrift.ttypes import Operation as ThriftOperation
from CHRLINE.services.thrift.ttypes import OpType
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BigInteger, Integer, String

from database.engine import Base, Session
from database.models.message import Message


class Operation(Base):
    query = Session.query_property()

    revision = Column(Integer, nullable=False)
    created_time = Column(BigInteger, nullable=False)
    type = Column(Integer, nullable=False)
    type_name = Column(String(255))
    req_seq = Column(Integer, nullable=False)
    checksum = Column(Integer)
    status = Column(Integer)
    param1 = Column(String(255))
    param2 = Column(String(255))
    param3 = Column(String(255))

    message_id = Column(Integer, ForeignKey("messages.id"))

    message = relationship(
        "Message", backref=backref("operation", uselist=False)
    )

    @classmethod
    def from_line_operation(cls, to: ThriftOperation) -> Operation:
        o = cls()
        o.revision = to.revision
        o.created_time = to.createdTime
        o.type = to.type
        o.type_name = OpType._VALUES_TO_NAMES.get(to.type, "")  # type:ignore
        o.req_seq = to.reqSeq
        o.checksum = to.checksum
        o.status = to.status
        o.param1 = to.param1
        o.param2 = to.param2
        o.param3 = to.param3

        if isinstance(to.message, ThriftMessage):
            o.message = Message.from_line_message(to.message)
            o.message.create()

        return o
