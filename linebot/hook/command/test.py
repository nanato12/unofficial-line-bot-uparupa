from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer
from CHRLINE.services.thrift.ttypes import Contact, Message

from linebot import LINEBot
from linebot.flex.profile import ProfileFlex
from linebot.logger import get_file_path_logger
from repository.user_repository import get_or_create_user_from_contact

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class TestCommandHook(HooksTracer):
    @tracer.Command(inpart=True)
    def test(self, msg: Message, bot: CHRLINE) -> None:
        """Test."""

        c: Contact = bot.getContact(str(msg._from))
        u = get_or_create_user_from_contact(c)

        bot.sendLiff(
            msg.to,
            ProfileFlex(u).build_message(),
        )
