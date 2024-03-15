from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer

from design.singleton import SingletonMeta
from linebot.parser import ConfigParser


class LINEBot(metaclass=SingletonMeta):
    auth_token: str
    tracer: HooksTracer

    def __init__(self) -> None:
        parser: ConfigParser = ConfigParser()
        c = CHRLINE(parser.token, device=parser.device, useThrift=True)
        self.auth_token = c.authToken
        self.tracer = HooksTracer(c)
