from typing import Optional

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message, MIDType

from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class CommonCommandHook(HooksTracerWrapper):
    @tracer.Command()
    def mid(self, msg: Message, bot: CHRLINE) -> None:
        """
        送信者のmidを送信します。
        メンションすることでメンションした人のmidを送信します。
        """

        bot.replyMessage(msg, str(msg._from))

    @tracer.Command(toType=[MIDType.GROUP])
    def gid(self, msg: Message, bot: CHRLINE) -> None:
        """
        グループのIDを送信します。
        """

        bot.replyMessage(msg, str(msg.to))

    @tracer.Command()
    def help(self, msg: Message, bot: CHRLINE) -> None:
        """
        ヘルプを送信します。
        """

        bot.replyMessage(msg, self.genHelp())

    @tracer.Command()
    def unsend(self, msg: Message, bot: CHRLINE) -> None:
        """
        リプライ先のメッセージを取り消します。
        """

        unsend_msg_id: Optional[str] = msg.relatedMessageId
        if unsend_msg_id:
            bot.unsendMessage(unsend_msg_id)
        else:
            bot.replyMessage(msg, "取り消したいメッセージをリプライしてね！")
