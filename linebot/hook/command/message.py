from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message

from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper
from repository.message_repository import get_partial_match_messages

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class MessageCommandHook(HooksTracerWrapper):
    @tracer.Command(prefixes=False, inpart=True, alt=["文字カウント"])
    def word_count(self, msg: Message, bot: CHRLINE) -> None:
        """
        指定した文字列の出現回数をカウントするよ
        """

        text: str = msg.text
        if " " not in text:
            bot.replyMessage(msg, "文字カウント カウントしたい文字列")
            return

        target_text = text.split(" ")[1]
        messages = get_partial_match_messages(target_text)
        bot.replyMessage(
            msg,
            f"「{target_text}」が出現した回数は {len(messages)} 回だよ〜！",
        )
