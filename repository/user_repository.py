from typing import Optional

from CHRLINE.services.thrift.ttypes import Contact

from database.models.user import User


def find_user_from_mid(mid: str) -> Optional[User]:
    return User.query.filter(User.mid == mid).first()


def get_or_create_user_from_contact(c: Contact) -> User:
    u = find_user_from_mid(str(c.mid))
    if not u:
        u = User.from_line_contact(c)
        u.create()
    return u
