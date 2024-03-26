from CHRLINE import CHRLINE
from CHRLINE.exceptions import LineServiceException
from CHRLINE.services.thrift.ttypes import ContentType, Message, MIDType
from sqlalchemy import desc

from database.models.message import Message as MessageModel
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.user_hook_tracer import HooksTracerWrapper
from repository.keyword_repository import (
    choice_keyword,
    find_keywords_from_receive_text,
)
from repository.user_repository import get_or_create_user_from_mid

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class ContentHook(HooksTracerWrapper):
    @tracer.Content(ContentType.NONE)
    def text_message(self, msg: Message, bot: CHRLINE) -> None:
        logger.info(msg.text)

        # 直近の同じ送信者の同じテキストを探す
        recent_message = (
            MessageModel.query.filter(MessageModel._from == msg._from)
            .order_by(desc(MessageModel.create_time))
            .first()
        )

        # 直近のメッセージから3秒以内だったら処理しない
        if (
            recent_message
            and (msg.createdTime - recent_message.create_time) < 3000
        ):
            logger.info("連投対策")
            return

        if tracer.trace(msg, self.HooksType["Command"], bot):
            return

        if (mid := str(msg.text).strip()).startswith("u") and len(mid) == 33:
            try:
                _ = bot.getContact(mid)
                bot.sendContact(msg.to, mid)
            except LineServiceException:
                pass
            except Exception as e:
                raise e

        # グループ以外はスルー
        if msg.toType != MIDType.GROUP:
            return

        if keywords := find_keywords_from_receive_text(msg.text):
            if k := choice_keyword(keywords):
                if k.reply_text:
                    bot.replyMessage(msg, k.reply_text)
                if k.reply_image_path:
                    bot.sendImage(msg.to, k.reply_image_path)
                if k.reply_voice_path:
                    bot.sendAudio(msg.to, k.reply_voice_path)

        u = get_or_create_user_from_mid(msg._from, bot)
        if u.can_give_exp(str(msg.text), str(msg.to)):
            if u.give_exp():
                bot.replyMessage(msg, f"レベルが「{u.level}」に上がったよ！")
