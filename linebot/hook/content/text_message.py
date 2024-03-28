from CHRLINE.exceptions import LineServiceException
from CHRLINE.services.thrift.ttypes import (
    Contact,
    ContentType,
    Message,
    MIDType,
)
from sqlalchemy import desc

from database.models.message import Message as MessageModel
from linebot.helpers.message import get_mids_from_message
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.models.emojis.mahjang import MahjangMUPEmoji
from linebot.models.emojis.slot_emoji import SlotEmoji
from linebot.wrappers.chrline_wrapper import CHRLINEWrapper
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper
from repository.keyword_repository import (
    choice_keyword,
    find_keywords_from_receive_text,
)
from repository.user_repository import (
    get_or_create_user_from_contact,
    get_or_create_user_from_mid,
)

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class TextMessageHook(HooksTracerWrapper):
    @tracer.Content(ContentType.NONE)
    def text_message(self, msg: Message, bot: CHRLINEWrapper) -> None:
        text: str = msg.text

        logger.info(text)

        # 直近の同じ送信者のメッセージを探す
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

        if (mid := text.strip()).startswith("u") and len(mid) == 33:
            try:
                _ = bot.getContact(mid)
                bot.sendContact(msg.to, mid)
            except LineServiceException:
                pass
            except Exception as e:
                raise e

        if msg.toType != MIDType.GROUP:
            return

        if mentionee_mids := get_mids_from_message(msg):
            if text.endswith("プロフ"):
                u = get_or_create_user_from_mid(mentionee_mids[0], bot)
                bot.reply_user_profile(msg, u)
                return

        if keywords := find_keywords_from_receive_text(text):
            if k := choice_keyword(keywords):
                if k.reply_text:
                    reply_text: str = k.reply_text
                    if "[name]" in reply_text:
                        c: Contact = bot.getContact(msg._from)
                        reply_text = reply_text.replace(
                            "[name]", c.displayName
                        )
                    if "@!" in reply_text:
                        bot.sendMention(msg.to, reply_text, mids=[msg._from])
                    elif reply_text.startswith("/slot "):
                        bot.reply_emojis_message(
                            msg,
                            *SlotEmoji.convert_message(
                                list(reply_text.replace("/slot ", ""))
                            ),
                        )
                    elif reply_text.startswith("/mj "):
                        bot.reply_emojis_message(
                            msg,
                            *MahjangMUPEmoji.convert_message(
                                reply_text.replace("/mj ", "").split(" ")
                            ),
                        )
                    else:
                        bot.replyMessage(msg, reply_text)
                if k.reply_image_path:
                    bot.sendImage(msg.to, k.reply_image_path)
                if k.reply_voice_path:
                    bot.sendAudio(msg.to, k.reply_voice_path)

        u = get_or_create_user_from_mid(msg._from, bot)
        if u.can_give_exp(text, msg.to):
            if u.give_exp():
                bot.replyMessage(
                    msg,
                    f"レベルが「{u.level}」に上がったよ！\n"
                    "「プロフ」で自分のレベルが見られるよ！",
                )

        # 直近のメッセージから1時間経過していればユーザー情報を更新する
        if (
            recent_message
            and (msg.createdTime - recent_message.create_time)
            >= 60 * 60 * 1000
        ):
            c = bot.getContact(msg._from)
            user = get_or_create_user_from_contact(c)
            user.picture_status = c.pictureStatus
            user.save()

            logger.info(f"プロフィール更新: {msg._from}")
