from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message, MIDType

from linebot.flex.profile import ProfileFlex
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

    @tracer.Command(prefixes=False)
    def プロフ(self, msg: Message, bot: CHRLINE) -> None:
        """
        プロフィールを送信します。
        """

        bot.sendLiff(
            msg.to,
            ProfileFlex(self.user).build_message(),
        )
