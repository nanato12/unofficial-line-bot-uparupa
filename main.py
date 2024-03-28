from logging import ERROR, INFO, StreamHandler, basicConfig, getLogger
from logging.handlers import TimedRotatingFileHandler
from os import environ, makedirs

from linebot import hook  # noqa: F401
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger
from linebot.parser import ConfigParser

LOG_DIRECTORY = "logs"

logger = get_file_path_logger(__name__)
parser = ConfigParser()

if __name__ == "__main__":
    makedirs(LOG_DIRECTORY, exist_ok=True)

    basicConfig(
        level=INFO,
        datefmt="%Y/%m/%d %H:%M:%S",
        format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)s %(message)s",
        handlers=[
            TimedRotatingFileHandler(
                f"{LOG_DIRECTORY}/{parser.log_name}.log",
                when="midnight",
                backupCount=30,
                interval=1,
                encoding="utf-8",
            ),
            StreamHandler(),
        ],
    )

    # 外部モジュールのロガー
    getLogger("httpx").setLevel(ERROR)

    if environ.get("IS_LOCAL"):
        getLogger("sqlalchemy.engine").setLevel(INFO)

    line = LINEBot()
    line.tracer.run()
