from __future__ import annotations

from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message, MIDType

from database.helpers import bulk_create
from database.models.mention_check_log import MentionCheckLog
from database.models.operation import Message as MessageModel
from linebot.helpers.message import (
    get_mids_from_message,
    is_all_mention_message,
)
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper
from repository.message_repository import get_mention_message
from repository.user_repository import get_or_create_user_from_mid

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class MessageReadCommandHook(HooksTracerWrapper):
    @tracer.Command(
        prefixes=False,
        alt=["メンションチェック", "めんかく"],
        toType=[MIDType.GROUP, MIDType.ROOM],
    )
    def mention_check(self, msg: Message, bot: CHRLINE) -> None:
        """
        メンションされた箇所を確認するよ！
        """

        user = get_or_create_user_from_mid(msg._from, bot)
        mention_check_logs: list[MentionCheckLog] = user.mention_check_logs
        checked_message_ids = [log.message_id for log in mention_check_logs]

        messages = get_mention_message(msg._from, msg.to, checked_message_ids)

        mentionee_messages: list[MessageModel] = []
        for m in messages:
            if is_all_mention_message(m):
                mentionee_messages.append(m)
            elif msg._from in get_mids_from_message(m):
                mentionee_messages.append(m)

        if not mentionee_messages:
            bot.replyMessage(msg, "メンションされたメッセージはないよ！")
            return

        bot.replyMessage(msg, "最新5件のメンションをリプライするよ〜！")
        for m in mentionee_messages[-5:]:
            bot.replyMessage(m.to_thrift_message(), "ここ")

        logs: list[MentionCheckLog] = []
        for m in mentionee_messages:
            log = MentionCheckLog()
            log.message_id = m.id
            log.user_id = user.id
            logs.append(log)

        bulk_create(logs)
