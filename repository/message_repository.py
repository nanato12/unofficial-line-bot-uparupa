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


def get_partial_match_messages(word: str) -> list[Message]:
    return Message.query.where(Message.text.like(f"%{word}%")).all()  # type: ignore[no-any-return]


def get_mention_message(
    mid: str, to: str, exclude_message_ids: list[int]
) -> list[Message]:
    return (  # type: ignore [no-any-return]
        Message.query.filter(Message.to == to)
        .filter(Message._from != mid)
        .filter(Message.content_metadata.like("%MENTIONEES%"))
        .filter(Message.id.not_in(exclude_message_ids))
        .all()
    )
