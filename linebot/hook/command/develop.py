from CHRLINE import CHRLINE
from CHRLINE.services.thrift.ttypes import Message

from linebot.flex.test import TestFlex
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class DevelopCommandHook(HooksTracerWrapper):
    @tracer.Command(prefixes=False, alt=["テスト", "てすと"])
    def test(self, msg: Message, bot: CHRLINE) -> None:
        """
        テスト
        """

        logger.info(
            bot.sendLiff(
                msg.to,
                TestFlex().build_message(),
                liffId="1626444543-G6O9lb5v",
            )
        )
