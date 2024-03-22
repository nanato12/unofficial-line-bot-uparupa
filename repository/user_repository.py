from typing import Optional

from CHRLINE import CHRLINE
from sqlalchemy import desc

from constants.enums.authority import Authority
from database.models.user import User
from linebot.exceptions.sql_error import NotFoundRecordError


def find_user_from_mid(mid: str) -> Optional[User]:
    return User.query.filter(User.mid == mid).first()  # type: ignore[no-any-return]


def get_user_from_mid(mid: str) -> User:
    u = find_user_from_mid(str(mid))
    if not u:
        raise NotFoundRecordError(f"mid: '{mid}' is not found.")
    return u


def get_or_create_user_from_mid(mid: str, bot: CHRLINE) -> User:
    u = find_user_from_mid(mid)
    if not u:
        u = User.from_line_contact(bot.getContact(mid))
        u.create()
    return u


def get_ranked_users() -> list[User]:
    return (
        User.query.filter(User.authority != Authority.ADMIN)
        .order_by(desc(User.level))
        .order_by(desc(User.exp))
        .order_by(desc(User.created_at))
        .all()
    )
