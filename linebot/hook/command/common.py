from typing import Optional

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message, MIDType

from database.models.message import Message as MessageModel
from gpt import GPT
from gpt.message import Message as GPTMessage
from gpt.model import Model
from gpt.role import Role
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

    @tracer.Command(inpart=True)
    def gpt(self, msg: Message, bot: CHRLINE) -> None:
        """
        ChatGPTに質問を投げられます。
        リプライでも使用可能です。
        """

        text: str = msg.text

        if reply_message_id := msg.relatedMessageId:
            reply_message = MessageModel.query.filter(
                MessageModel.message_id == reply_message_id
            ).first()
            if not reply_message:
                bot.replyMessage(
                    msg, "リプライ先のメッセージが見つからなかったよ😭"
                )
                return

            text = f"{reply_message.text}\n\n" + text.replace("/gpt", "")

        gpt = GPT(
            Model.GPT_35_TURBO,
            [
                GPTMessage(
                    Role.SYSTEM,
                    "あなたは うぱるぱ という名前です。"
                    "あなたはYouChatではなく、うぱるぱです。",
                )
            ],
        )

        gpt.add_user_message(text)
        bot.replyMessage(msg, gpt.create())
