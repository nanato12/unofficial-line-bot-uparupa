from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message

from database.models.keyword import Keyword
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.user_hook_tracer import HooksTracerWrapper
from repository.keyword_repository import (
    check_registration_keyword,
    find_keyword_from_user_and_text,
)

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class KeywordCommandHook(HooksTracerWrapper):
    @tracer.Command(prefixes=False, inpart=True, alt=["キーワード登録"])
    def add_keyword(self, msg: Message, bot: CHRLINE) -> None:
        """キーワード登録ができます。
        キーワード登録 テキスト:返信
        """
        text: str = msg.text
        if " " not in text or ":" not in text:
            bot.replyMessage(
                msg, "不正なコマンドです！\n\nキーワード登録 テキスト:返信"
            )
            return

        targets = [s.strip() for s in text[text.index(" ") :].split(":")]
        receive_text = targets[0]
        reply_text = targets[1]

        if len(receive_text) < 3 or len(reply_text) < 1:
            bot.replyMessage(
                msg,
                "テキストは3文字以上、返信は1文字以上で登録してね！",
            )
            return

        if check_registration_keyword(self.user, receive_text):
            bot.replyMessage(
                msg, "あなたはすでにそのキーワードを登録しています！"
            )
            return

        k = Keyword()
        k.receive_text = receive_text
        k.reply_text = reply_text
        k.registrant = self.user
        k.create()

        bot.replyMessage(
            msg,
            f"送信: {receive_text}\n\n返信: {reply_text}\n\nで登録が完了しました。",
        )

    @tracer.Command(prefixes=False, inpart=True, alt=["キーワード削除"])
    def delete_keyword(self, msg: Message, bot: CHRLINE) -> None:
        """キーワード削除ができます。
        キーワード削除 テキスト
        """
        text: str = msg.text
        if " " not in text:
            bot.replyMessage(
                msg, "不正なコマンドです！\n\nキーワード削除 テキスト"
            )
            return

        word = text[text.index(" ") :].strip()
        if not (k := find_keyword_from_user_and_text(self.user, word)):
            bot.replyMessage(
                msg,
                f"あなたは「{word}」に対するキーワードを登録していません！",
            )
            return

        k.query.delete()

        bot.replyMessage(
            msg,
            f"あなたが登録した「{word}」に対するキーワードが削除されました！",
        )
