from CHRLINE.services.thrift.ttypes import Message

from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.chrline_wrapper import CHRLINEWrapper
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper
from repository.user_repository import (
    find_user_from_name,
    get_or_create_user_from_mid,
)

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class UserProfileCommandHook(HooksTracerWrapper):
    @tracer.Command(prefixes=False, alt=["プロフィール", "プロフ", "/me"])
    def profile(self, msg: Message, bot: CHRLINEWrapper) -> None:
        """
        プロフィールを送信します。
        """

        u = get_or_create_user_from_mid(msg._from, bot)
        bot.reply_user_profile(msg, u)

    @tracer.Command(alt=["名前", "名前変更"], prefixes=False, inpart=True)
    def name(self, msg: Message, bot: CHRLINEWrapper) -> None:
        """
        名前を変更します。
        """

        text: str = msg.text
        if " " not in text:
            bot.replyMessage(
                msg, "不正なコマンドです！\n\n名前 {変更したい名前}"
            )
            return

        name = text[text.index(" ") :].strip()
        if len(name) < 1 or len(name) > 8:
            bot.replyMessage(msg, "名前は1文字以上8文字以下にしてください！")
            return

        if find_user_from_name(name):
            bot.replyMessage(msg, "その名前はすでに登録されています！")
            return

        u = get_or_create_user_from_mid(msg._from, bot)
        u.name = name
        u.save()

        bot.replyMessage(msg, "名前を変更したよ♪")
