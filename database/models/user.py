from __future__ import annotations

from typing import Optional
from urllib.parse import urljoin

from CHRLINE.config import Config
from CHRLINE.services.thrift.ttypes import Contact as ThriftContact
from sqlalchemy import Enum, Text, text
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from constants.enums.authority import Authority
from database.engine import Base, Session
from linebot.config import Config as LINEBotConfig


class User(Base):
    query = Session.query_property()

    mid = Column(String(50), nullable=False)
    name = Column(
        String(20), nullable=False, default="noname", server_default="noname"
    )
    picture_status = Column(Text)
    level = Column(
        Integer, nullable=False, default=1, server_default=text("1")
    )
    exp = Column(Integer, nullable=False, default=0, server_default=text("0"))
    authority = Column(
        Enum(Authority),
        nullable=False,
        default=Authority.NORMAL,
        server_default=Authority.NORMAL.name,
    )

    @property
    def profile_url(self) -> Optional[str]:
        if self.picture_status is None:
            return None

        url: str = urljoin(
            Config.LINE_PROFILE_CDN_DOMAIN, str(self.picture_status)
        )
        return url

    @classmethod
    def from_line_contact(cls, tc: ThriftContact) -> User:
        u = cls()
        u.mid = tc.mid
        u.picture_status = tc.pictureStatus
        if tc.mid in LINEBotConfig.ADMINS:
            u.authority = Authority.ADMIN
        return u
