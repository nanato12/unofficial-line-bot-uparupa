from CHRLINE.services.thrift.ttypes import OpType
from sqlalchemy import asc, func

from database.models.message import Message
from database.models.operation import Operation


def get_read_message_ops(message_id: str) -> list[Operation]:
    message = Message.query.filter(Message.message_id == message_id).first()
    if not message:
        return []

    return (  # type: ignore[no-any-return]
        Operation.query.filter(Operation.type == OpType.NOTIFIED_READ_MESSAGE)
        .filter(Operation.param1 == message.to)
        .filter(Operation.param2 != message._from)
        .filter(Operation.created_time >= message.create_time)
        .group_by(Operation.param2)
        .with_entities(
            func.min(Operation.created_at).label("created_at"),
            Operation.param2,
        )
        .order_by(asc("created_at"))
        .all()
    )
