from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer
from CHRLINE.services.thrift.ttypes import Message

from linebot import LINEBot
from linebot.logger import get_file_path_logger

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class HelpCommandHook(HooksTracer):
    @tracer.Command()
    def ヘルプ(self, msg: Message, bot: CHRLINE) -> None:
        """ヘルプを送信"""

        bot.replyMessage(msg, self.genHelp())
