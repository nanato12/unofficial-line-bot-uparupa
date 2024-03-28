from json import dumps as json_dumps

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message

from linebot.models.emojis import Emoji


class CHRLINEWrapper(CHRLINE):
    def reply_emojis_message(
        self, msg: Message, text: str, emojis: list[Emoji]
    ) -> Message:
        return self.replyMessage(
            msg,
            text,
            contentMetadata={
                "app_extension_type": "null",
                "PREVIEW_URL_ENABLED": "true",
                "app_version_code": "131720351",
                "REPLACE": json_dumps(
                    {
                        "sticon": {
                            "resources": [
                                emoji.to_resource_data() for emoji in emojis
                            ]
                        }
                    },
                    separators=(",", ":"),
                ),
                "STICON_OWNERSHIP": json_dumps(
                    list(set(emoji.__class__.product_id for emoji in emojis)),
                    separators=(",", ":"),
                ),
            },
        )
