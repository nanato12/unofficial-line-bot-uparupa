from datetime import datetime
from json import loads as json_loads

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message, MIDType

from database.models.user import User
from linebot.flex.profile import ProfileFlex
from linebot.helpers.calculation import calc_need_exp
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.user_hook_tracer import HooksTracerWrapper

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

    @tracer.Command(prefixes=False, alt=["プロフィール", "プロフ"])
    def profile(self, msg: Message, bot: CHRLINE) -> None:
        """
        プロフィールを送信します。
        """

        logger.info(
            r := bot.sendLiff(
                msg.to,
                ProfileFlex(self.user).build_message(),
            )
        )

        if json_loads(r).get("status") != "ok":
            u: User = self.user
            bot.replyMessage(
                msg,
                (
                    f"Ranking: {u.ranking}\n"
                    f"権限: {u.authority.name}\n"
                    f"レベル: {u.level}\n"
                    f"経験値: {u.exp:,} / {calc_need_exp(u.level):,}"
                ),
            )
