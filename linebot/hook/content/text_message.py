from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer
from CHRLINE.services.thrift.ttypes import Contact, ContentType, Message

from database.models.user import User
from linebot import LINEBot
from linebot.logger import get_file_path_logger
from repository.user_repository import find_user_from_mid

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class ContentHook(HooksTracer):
    @tracer.Content(ContentType.NONE)
    def text_message(self, msg: Message, bot: CHRLINE) -> None:
        if tracer.trace(msg, self.HooksType["Command"], bot):
            return

        sender_mid = str(msg._from)

        user = find_user_from_mid(sender_mid)
        if not user:
            c: Contact = bot.getContact(sender_mid)
            user = User.from_line_contact(c)
            user.save()

        logger.info(msg.text)
