from typing import Optional

from sqlalchemy import desc

from database.models.message import Message


def find_user_group_last_message(mid: str, gid: str) -> Optional[Message]:
    return (  # type: ignore[no-any-return]
        Message.query.filter(Message._from == mid)
        .filter(Message.to == gid)
        .order_by(desc(Message.created_at))
        .first()
    )
