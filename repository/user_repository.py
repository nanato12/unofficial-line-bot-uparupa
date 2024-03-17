from typing import Optional

from CHRLINE.services.thrift.ttypes import Contact

from database.models.user import User
from repository.exceptions import NotFoundRecordError


def find_user_from_mid(mid: str) -> Optional[User]:
    return User.query.filter(User.mid == mid).first()  # type: ignore


def get_user_from_mid(mid: str) -> User:
    u = find_user_from_mid(str(mid))
    if not u:
        raise NotFoundRecordError(f"mid: '{mid}' is not found.")
    return u


def get_or_create_user_from_contact(c: Contact) -> User:
    u = find_user_from_mid(str(c.mid))
    if not u:
        u = User.from_line_contact(c)
        u.create()
    return u
