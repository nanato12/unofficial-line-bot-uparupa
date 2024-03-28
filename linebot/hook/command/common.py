from datetime import datetime
from json import loads as json_loads
from typing import Optional

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message, MIDType

from linebot.flex.profile import ProfileFlex
from linebot.helpers.calculation import calc_need_exp
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper
from repository.user_repository import (
    find_user_from_name,
    get_or_create_user_from_mid,
)

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
    def contact(self, msg: Message, bot: CHRLINE) -> None:
        """
        /contact {mid} で mid の連絡先を送信します。
        """

        bot.replyMessage(msg, str(msg._from))

    @tracer.Command()
    def help(self, msg: Message, bot: CHRLINE) -> None:
        """
        ヘルプを送信します。
        """

        bot.replyMessage(msg, self.genHelp())

    @tracer.Command()
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

    @tracer.Command()
    def unsend(self, msg: Message, bot: CHRLINE) -> None:
        """
        リプライ先のメッセージを取り消します。
        """

        unsend_msg_id: Optional[str] = msg.relatedMessageId
        if unsend_msg_id:
            bot.unsendMessage(unsend_msg_id)
            bot.replyMessage(msg, "メッセージを取り消したよ！")
        else:
            bot.replyMessage(msg, "取り消したいメッセージをリプライしてね！")

    @tracer.Command(prefixes=False, alt=["プロフィール", "プロフ", "/me"])
    def profile(self, msg: Message, bot: CHRLINE) -> None:
        """
        プロフィールを送信します。
        """

        u = get_or_create_user_from_mid(msg._from, bot)

        logger.info(
            r := bot.sendLiff(
                msg.to,
                ProfileFlex(u).build_message(),
                liffId="1626444543-G6O9lb5v",
            )
        )

        if json_loads(r).get("status") != "ok":
            bot.replyMessage(
                msg,
                (
                    f"Ranking: {u.ranking}\n"
                    f"権限: {u.authority.name}\n"
                    f"レベル: {u.level}\n"
                    f"経験値: {u.exp:,} / {calc_need_exp(u.level):,}"
                ),
            )

    @tracer.Command(alt=["名前", "名前変更"], prefixes=False, inpart=True)
    def name(self, msg: Message, bot: CHRLINE) -> None:
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
