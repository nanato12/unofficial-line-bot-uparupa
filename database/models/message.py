from __future__ import annotations

from CHRLINE.services.thrift.ttypes import Location as ThriftLocation
from CHRLINE.services.thrift.ttypes import Message as ThriftMessage
from sqlalchemy import LargeBinary
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import JSON, BigInteger, Boolean, Integer, String, Text

from database.engine import Base, Session
from database.models.location import Location


class Message(Base):
    query = Session.query_property()

    _from = Column(String(50), name="from", nullable=False)
    to = Column(String(50), nullable=False)
    to_type = Column(Integer, nullable=False)
    create_time = Column(BigInteger, nullable=False)
    delivered_time = Column(BigInteger)
    text = Column(Text)
    location_id = Column(Integer, ForeignKey("locations.id"))
    has_content = Column(Boolean)
    content_type = Column(Integer)
    content_preview = Column(LargeBinary)
    content_metadata = Column(JSON, nullable=False, default={})
    session_id = Column(Integer)
    message_id = Column(String(50))
    chunks = Column(JSON, nullable=False, default=[])
    relation_message_id = Column(String(255))
    message_relation_type = Column(Integer)
    read_count = Column(Integer)
    related_message_service_code = Column(Integer)
    reactions = Column(JSON, nullable=False, default=[])
    op_type = Column(Integer)
    is_e2ee = Column(Boolean)

    location = relationship(
        "Location", backref=backref("message", uselist=False)
    )

    def to_thrift_message(self) -> ThriftMessage:
        m = ThriftMessage(
            id=self.message_id,
            _from=self._from,
            to=self.to,
            toType=self.to_type,
            contentMetadata=self.content_metadata,
            relatedMessageId=self.relation_message_id,
        )
        m.opType = self.op_type
        m.isE2EE = self.is_e2ee
        return m

    @classmethod
    def from_line_message(cls, msg: ThriftMessage) -> Message:
        m = cls()
        m._from = msg._from
        m.to = msg.to
        m.to_type = msg.toType
        m.create_time = msg.createdTime
        m.delivered_time = msg.deliveredTime
        m.text = msg.text

        if isinstance(msg.location, ThriftLocation):
            m.location = Location.from_line_location(msg.location)
            m.location.create()

        m.has_content = msg.hasContent
        m.content_type = msg.contentType
        m.content_preview = msg.contentPreview
        m.content_metadata = msg.contentMetadata
        m.session_id = msg.sessionId
        m.message_id = msg.id
        # TODO: list[bytes] のため、使用不可
        # m.chunks = msg.chunks
        m.relation_message_id = msg.relatedMessageId
        m.message_relation_type = msg.messageRelationType
        m.read_count = msg.readCount
        m.related_message_service_code = msg.relatedMessageServiceCode
        m.reactions = msg.reactions
        m.op_type = msg.opType  # type:ignore
        m.is_e2ee = msg.isE2EE  # type:ignore

        return m
