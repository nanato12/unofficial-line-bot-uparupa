from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer

from design.singleton import SingletonMeta
from linebot.config import Config
from linebot.parser import ConfigParser


class LINEBot(metaclass=SingletonMeta):
    auth_token: str
    bot: CHRLINE
    tracer: HooksTracer

    def __init__(self) -> None:
        parser: ConfigParser = ConfigParser()

        self.bot = CHRLINE(parser.token, device=parser.device, useThrift=True)
        self.auth_token = self.bot.authToken

        for mid in Config.ADMINS:
            self.bot.sendMessage(mid, "起動したよ♪")

        self.tracer = HooksTracer(self.bot, prefixes=["/"])
