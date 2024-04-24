from CHRLINE.services.thrift.ttypes import ContentType, Message, MIDType

from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.chrline_wrapper import CHRLINEWrapper
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class ContactHook(HooksTracerWrapper):
    @tracer.Content(ContentType.CONTACT)
    def chat_event(self, msg: Message, bot: CHRLINEWrapper) -> None:
        if msg.contentMetadata is None:
            return

        if msg.toType in [MIDType.GROUP, MIDType.ROOM]:
            to = msg.to
        else:
            to = msg._from

        bot.sendMessage(to, msg.contentMetadata.get("mid", "mid不明"))
