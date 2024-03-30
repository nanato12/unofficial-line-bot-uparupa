from constants.enums.authority import Authority
from design.singleton import SingletonMeta
from linebot.config import Config
from linebot.parser import ConfigParser
from linebot.wrappers.chrline_wrapper import CHRLINEWrapper
from linebot.wrappers.hook_tracer_wrapper import HooksTracerWrapper


class LINEBot(metaclass=SingletonMeta):
    auth_token: str
    bot: CHRLINEWrapper
    tracer: HooksTracerWrapper

    def __init__(self) -> None:
        parser: ConfigParser = ConfigParser()

        self.bot = CHRLINEWrapper(
            parser.token,
            device=parser.device,
            useThrift=True,
            savePath="./",
        )
        self.auth_token = self.bot.authToken

        for mid in Config.ADMINS:
            self.bot.sendMessage(mid, "起動したよ♪")

        self.tracer = HooksTracerWrapper(self.bot, prefixes=["/"])

        for mid in Config.ADMINS:
            self.tracer.addPermission(mid, Authority.ADMIN)
