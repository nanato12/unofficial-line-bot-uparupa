from json import loads as json_loads

from CHRLINE.services.thrift.ttypes import Message


def get_mids_from_message(msg: Message) -> list[str]:
    if not isinstance(msg.contentMetadata, dict):
        return []

    mention_data: dict[str, list[dict[str, str]]] = json_loads(
        msg.contentMetadata.get("MENTION", "{}")
    )

    return [
        mentionee["M"]
        for mentionee in mention_data.get("MENTIONEES", [])
        if mentionee.get("M")
    ]
