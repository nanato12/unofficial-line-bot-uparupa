from typing import Optional

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Contact

from database.models.user import User
from linebot.exceptions.sql_error import NotFoundRecordError


def find_user_from_mid(mid: str) -> Optional[User]:
    return User.query.filter(User.mid == mid).first()  # type: ignore[no-any-return]


def get_user_from_mid(mid: str) -> User:
    u = find_user_from_mid(str(mid))
    if not u:
        raise NotFoundRecordError(f"mid: '{mid}' is not found.")
    return u


def get_or_create_user_from_contact(c: Contact) -> User:
    u = find_user_from_mid(c.mid)
    if not u:
        u = User.from_line_contact(c)
        u.create()
    return u


def get_or_create_user_from_mid(mid: str, bot: CHRLINE) -> User:
    u = find_user_from_mid(mid)
    if not u:
        u = User.from_line_contact(bot.getContact(mid))
        u.create()
    return u


def find_user_from_name(n: str) -> Optional[User]:
    return User.query.filter(User.name == n).first()  # type: ignore[no-any-return]
