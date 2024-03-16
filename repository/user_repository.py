from typing import Optional

from database.models.user import User


def find_user_from_mid(mid: str) -> Optional[User]:
    return User.query.filter(User.mid == mid).first()
