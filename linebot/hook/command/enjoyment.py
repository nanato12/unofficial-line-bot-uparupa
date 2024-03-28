from random import choice as random_choice

from CHRLINE.services.thrift.ttypes import Message

from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.chrline_wrapper import CHRLINEWrapper
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class EnjoymentCommandHook(HooksTracerWrapper):
    @tracer.Command(prefixes=False, alt=["うぱるぱ"])
    def uparupa(self, msg: Message, bot: CHRLINEWrapper) -> None:
        """
        うぱるぱが反応します。
        """

        REPLY_WORDS = [
            "ん？",
            "なに〜？",
            "なに？！",
            "なに？？？",
            "どうした？",
            "どしたん？\n話聞こか？\nうんうん、それは彼氏が悪いね\n僕なら絶対そんな思いはさせない",
        ]

        bot.replyMessage(msg, random_choice(REPLY_WORDS))
