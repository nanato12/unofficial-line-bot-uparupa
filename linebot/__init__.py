from threading import Thread
from time import sleep

from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer

from design.singleton import SingletonMeta
from linebot.parser import ConfigParser


class LINEBot(metaclass=SingletonMeta):
    auth_token: str
    bot: CHRLINE
    tracer: HooksTracer

    def __init__(self) -> None:
        parser: ConfigParser = ConfigParser()

        self.bot = CHRLINE(parser.token, device=parser.device, useThrift=True)
        self.auth_token = self.bot.authToken
        self.tracer = HooksTracer(self.bot, prefixes=["/"])

        t = Thread(target=self.noop)
        t.daemon = True
        t.start()

    def noop(self) -> None:
        self.bot.noop()
        sleep(20)
