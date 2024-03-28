from random import sample as random_sample

from CHRLINE.services.thrift.ttypes import Message

from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.models.emojis.mahjang import PAI, MahjangMUPEmoji
from linebot.models.emojis.slot_emoji import SlotEmoji
from linebot.wrappers.chrline_wrapper import CHRLINEWrapper
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class EmojiCommandHook(HooksTracerWrapper):
    @tracer.Command(inpart=True)
    def slot(self, msg: Message, bot: CHRLINEWrapper) -> None:
        """
        Solt絵文字を送信します
        """
        text: str = msg.text
        target_text = text[text.index(" ") :].strip()

        if len(target_text) == 0:
            bot.replyMessage(msg, "不正なコマンドです！\n\n/slot 文字列")
            return

        if " " in target_text:
            texts = target_text.split(" ")
        else:
            texts = list(target_text)
        bot.reply_emojis_message(msg, *SlotEmoji.convert_message(texts))

    @tracer.Command(inpart=True)
    def mj(self, msg: Message, bot: CHRLINEWrapper) -> None:
        """
        麻雀絵文字を送信します
        """
        text: str = msg.text
        target_text = text[text.index(" ") :].strip()

        if len(target_text) == 0:
            bot.replyMessage(msg, "不正なコマンドです！\n\n/mj 文字列")
            return

        bot.reply_emojis_message(
            msg, *MahjangMUPEmoji.convert_message(target_text.split(" "))
        )

    @tracer.Command(prefixes=False, alt=["ななといつ"])
    def nanato12(self, msg: Message, bot: CHRLINEWrapper) -> None:
        """
        七対子を送信します
        """
        pai = random_sample(PAI, k=7)
        pai = sorted(pai + pai)
        bot.reply_emojis_message(msg, *MahjangMUPEmoji.convert_message(pai))
