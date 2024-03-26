from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional
from urllib.parse import urljoin

from CHRLINE.config import Config
from CHRLINE.services.thrift.ttypes import Contact as ThriftContact
from sqlalchemy import Enum, Text, desc, text
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from constants.enums.authority import Authority
from database.engine import Base, Session
from linebot.config import Config as LINEBotConfig
from linebot.helpers.calculation import calc_need_exp, random_exp
from repository.message_repository import find_user_group_last_message


class User(Base):
    query = Session.query_property()

    mid = Column(String(50), nullable=False)
    name = Column(
        String(20), nullable=False, default="noname", server_default="noname"
    )
    picture_status = Column(Text)
    level: int = Column(
        Integer, nullable=False, default=1, server_default=text("1")
    )
    exp = Column(Integer, nullable=False, default=0, server_default=text("0"))
    authority: Authority = Column(
        Enum(Authority),
        nullable=False,
        default=Authority.NORMAL,
        server_default=Authority.NORMAL.name,
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(Base, self).__init__(*args, **kwargs)  # type: ignore
        self.name = "noname"
        self.level = 1
        self.exp = 0

    def __lt__(self, u: User) -> bool:
        if self.authority != u.authority:
            return self.authority < u.authority  # type: ignore[no-any-return]
        if self.level != u.level:
            return self.level < u.level  # type: ignore[no-any-return]
        if self.exp != u.exp:
            return self.exp < u.exp  # type: ignore[no-any-return]
        return self.created_at < u.created_at  # type: ignore[no-any-return]

    def __gt__(self, u: User) -> bool:
        return not self.__lt__(u)

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

    @classmethod
    def get_ranked_users(cls) -> list[User]:
        return (  # type: ignore [no-any-return]
            cls.query.filter(User.authority != Authority.ADMIN)
            .order_by(desc(User.level))
            .order_by(desc(User.exp))
            .order_by(desc(User.created_at))
            .all()
        )

    @property
    def ranking(self) -> int:
        if self.authority == Authority.ADMIN:
            return 0

        return [u.mid for u in self.get_ranked_users()].index(self.mid) + 1

    def can_give_exp(self, text: str, gid: str) -> bool:
        last_message = find_user_group_last_message(self.mid, gid)
        if last_message is None or last_message.text is None:
            return True

        # 3種類以下ならNG
        if len(set(text)) <= 3:
            return False

        # 最終メッセージとの文字の種類さが3種類以下15種類以上ならNG
        cd = abs(len(set(last_message.text)) - len(set(text)))
        if cd <= 3 or cd >= 15:
            return False

        # 最終メッセージとの差分が5秒未満ならNG
        td: timedelta = datetime.now() - last_message.created_at
        if td.total_seconds() < 5:
            return False

        return True

    def give_exp(self, exp: Optional[int] = None) -> bool:
        result = False

        if exp is None:
            exp = random_exp()

        self.exp += exp
        while self.exp >= calc_need_exp(self.level):
            self.exp -= calc_need_exp(self.level)
            self.level += 1
            result = True
        self.save()

        return result
