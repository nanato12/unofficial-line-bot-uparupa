from datetime import datetime

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message

from constants.enums.authority import Authority
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class AdminMessageCommandHook(HooksTracerWrapper):
    @tracer.Command(permissions=[Authority.ADMIN])
    def msg(self, msg: Message, bot: CHRLINE) -> None:
        """
        メッセージIDを返します。
        """

        if reply_message_id := msg.relatedMessageId:
            bot.replyMessage(msg, reply_message_id)
            return

        bot.replyMessage(msg, msg.id)

    @tracer.Command(permissions=[Authority.ADMIN])
    def test(self, msg: Message, bot: CHRLINE) -> None:
        """
        起動確認を行います。
        """

        bot.replyMessage(
            msg,
            (
                "動いてるよ〜\n\n"
                f"経過時間: {str(datetime.now()-self.setup_timestamp)[:-7]}\n"
                f"起動日時: {self.setup_timestamp:%Y-%m-%d %H:%M:%S}"
            ),
        )
