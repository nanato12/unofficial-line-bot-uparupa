from CHRLINE.services.thrift.ttypes import OpType

from database.models.operation import Operation


def get_read_message_ops(message_id: str) -> list[Operation]:
    return (  # type: ignore[no-any-return]
        Operation.query.filter(Operation.type == OpType.NOTIFIED_READ_MESSAGE)
        .filter(Operation.param3 == message_id)
        .all()
    )
