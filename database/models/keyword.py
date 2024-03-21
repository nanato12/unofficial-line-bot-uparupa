from __future__ import annotations

from sqlalchemy import Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer

from database.engine import Base, Session


class Keyword(Base):
    query = Session.query_property()

    receive_text = Column(Text, nullable=False)
    reply_text = Column(Text, nullable=False)

    # ForeignKey
    registrant_id = Column(Integer, ForeignKey("users.id"))
    registrant = relationship(
        "User", backref=backref("keywords", uselist=True)
    )
