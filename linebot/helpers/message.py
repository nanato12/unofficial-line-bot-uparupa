from json import loads as json_loads

from CHRLINE.services.thrift.ttypes import Message

from database.models.operation import Message as MessageModel


def __get_mentionee(msg: Message | MessageModel) -> list[dict[str, str]]:
    if isinstance(msg, Message) and not isinstance(
        (metadata := msg.contentMetadata), dict
    ):
        return []
    elif isinstance(msg, MessageModel) and not isinstance(
        (metadata := msg.content_metadata), dict
    ):
        return []

    mention_data: dict[str, list[dict[str, str]]] = json_loads(
        metadata.get("MENTION", "{}")
    )
    return mention_data.get("MENTIONEES", [])


def get_mids_from_message(msg: Message) -> list[str]:
    return [
        mentionee["M"]
        for mentionee in __get_mentionee(msg)
        if mentionee.get("M")
    ]


def is_all_mention_message(msg: Message) -> bool:
    for mentionee in __get_mentionee(msg):
        if mentionee.get("A") == "1":
            return True
    return False
