from typing import Optional

from database.engine import session
from database.models.user import User


def find_user_from_mid(mid: str) -> Optional[User]:
    return session.query(User).filter(User.mid == mid).first()
