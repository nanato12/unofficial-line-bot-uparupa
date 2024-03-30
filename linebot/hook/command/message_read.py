from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Contact, Message

from database.models.operation import Operation
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper
from repository.operation_repository import get_read_message_ops

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


@dataclass
class MessageReader:
    created_at: datetime
    name: str

    @classmethod
    def from_ops(
        cls, ops: list[Operation], bot: CHRLINE
    ) -> list[MessageReader]:
        contacts: list[Contact] = bot.getContacts([op.param2 for op in ops])
        contact_map: dict[str, str] = {c.mid: c.displayName for c in contacts}
        return [cls(op.created_at, contact_map[op.param2]) for op in ops]


class MessageReadCommandHook(HooksTracerWrapper):
    @tracer.Command(prefixes=False, alt=["既読ポイント", "セット"])
    def read_point_set(self, msg: Message, bot: CHRLINE) -> None:
        """
        既読ポイントをセットするよ。
        「チェック」コマンドで誰が既読をつけたか確認できるよ。
        「チェック詳細」コマンドでもっと細かい確認ができるよ。
        """

        bot.replyMessage(
            msg,
            "既読をつけた人を確認したい時はこのメッセージに「チェック」とリプライしてね☺️\n"
            "うぱるぱが送ったメッセージならどれでも確認できるよ😉",
        )

    @tracer.Command(prefixes=False, alt=["既読ポイント確認", "チェック"])
    def read_point_check(self, msg: Message, bot: CHRLINE) -> None:
        """
        既読をつけたユーザーを確認できるよ。
        うぱるぱが送ったメッセージに「チェック」とリプライしてね😉
        """

        if not (reply_message_id := msg.relatedMessageId):
            return

        readers = MessageReader.from_ops(
            get_read_message_ops(reply_message_id), bot
        )
        if not readers:
            bot.replyMessage(msg, "既読をつけた人はいません😭")
            return

        bot.replyMessage(
            msg,
            "既読確認😉\n\n" + "\n".join([f"・{r.name}" for r in readers]),
        )

    @tracer.Command(
        prefixes=False, alt=["既読ポイント確認詳細", "チェック詳細"]
    )
    def read_point_check_detail(self, msg: Message, bot: CHRLINE) -> None:
        """
        「チェック」コマンドより詳細に確認できるよ😉
        """

        if not (reply_message_id := msg.relatedMessageId):
            return

        readers = MessageReader.from_ops(
            get_read_message_ops(reply_message_id), bot
        )
        if not readers:
            bot.replyMessage(msg, "既読をつけた人はいません😭")
            return

        bot.replyMessage(
            msg,
            (
                "既読確認😉\n\n"
                + "\n".join(
                    [f"・{r.name}\n{r.created_at}\n" for r in readers]
                ).strip()
            ),
        )
