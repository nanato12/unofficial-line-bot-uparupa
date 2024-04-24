from __future__ import annotations

from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer

from database.engine import Base, Session


class MentionCheckLog(Base):
    query = Session.query_property()

    __tablename__ = "mention_check_logs"

    # ForeignKey
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User", backref=backref("mention_check_logs", uselist=True)
    )

    message_id = Column(Integer, ForeignKey("messages.id"))
    message = relationship(
        "Message", backref=backref("mention_check_log", uselist=False)
    )
