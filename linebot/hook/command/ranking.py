from json import loads as json_loads

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message

from database.models.user import User
from linebot.flex.ranking import RankingFlex
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class RankingCommandHook(HooksTracerWrapper):
    @tracer.Command(prefixes=False, alt=["ランキング"])
    def ranking(self, msg: Message, bot: CHRLINE) -> None:
        """
        ランキングを送信します。
        """

        users = User.get_ranked_users()[:40]

        logger.info(
            r := bot.sendLiff(
                msg.to,
                RankingFlex(users).build_message(),
                liffId="1626444543-G6O9lb5v",
            )
        )

        if json_loads(r).get("status") != "ok":
            bot.replyMessage(
                msg,
                "\n".join(
                    [
                        f"{i}位 Lv.{user.level} {user.name}"
                        for i, user in enumerate(users[:10], start=1)
                    ]
                ),
            )
