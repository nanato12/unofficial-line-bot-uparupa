from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Contact, ContentType, Message

from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.user_hook_tracer import HooksTracerWrapper
from repository.user_repository import get_or_create_user_from_contact

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class ContentHook(HooksTracerWrapper):
    @tracer.Content(ContentType.NONE)
    def text_message(self, msg: Message, bot: CHRLINE) -> None:
        c: Contact = bot.getContact(str(msg._from))
        self.user = get_or_create_user_from_contact(c)

        if tracer.trace(msg, self.HooksType["Command"], bot):
            return

        logger.info(msg.text)
