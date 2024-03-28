from json import dumps as json_dumps
from json import loads as json_loads
from typing import Union

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message, MIDType

from database.models.user import User
from linebot.flex.profile import ProfileFlex
from linebot.helpers.calculation import calc_need_exp
from linebot.logger import get_file_path_logger
from linebot.models.emojis import Emoji

logger = get_file_path_logger(__name__)


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

    def reply_user_profile(self, msg: Message, u: User) -> Union[str, Message]:
        to: str = msg._from if msg.toType == MIDType.USER else msg.to

        logger.info(
            r := self.sendLiff(
                to,
                ProfileFlex(u).build_message(),
                liffId="1626444543-G6O9lb5v",
            )
        )

        if json_loads(r).get("status") != "ok":
            return self.replyMessage(
                msg,
                (
                    f"Ranking: {u.ranking}\n"
                    f"権限: {u.authority.name}\n"
                    f"レベル: {u.level}\n"
                    f"経験値: {u.exp:,} / {calc_need_exp(u.level):,}"
                ),
            )
        return r
