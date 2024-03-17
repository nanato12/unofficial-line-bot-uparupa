from argparse import ArgumentParser

from design.singleton import SingletonMeta
from linebot.helpers.config import get_config_by_name

DEFAULT_CONFIG_JSON = "config.json"


class ConfigParser(ArgumentParser, metaclass=SingletonMeta):
    device: str = ""
    token: str = ""
    log_name: str = ""
    db_host: str = ""
    db_port: str = ""
    db_user: str = ""
    db_password: str = ""
    db_database: str = ""
    db_charset: str = ""

    def __init__(self) -> None:
        super().__init__()
        self.add_argument("-c", "--config-name", default="", help="設定名")

        # linebot arguments
        self.add_argument("-d", "--device", help="デバイス名")
        self.add_argument("-t", "--token", help="トークン")
        self.add_argument("-l", "--log-name", help="ログファイル名")

        # database arguments
        self.add_argument(
            "-dh", "--db-host", default="127.0.0.1", help="DBのホスト"
        )
        self.add_argument(
            "-dp", "--db-port", default="3306", help="DBのポート"
        )
        self.add_argument(
            "-du", "--db-user", default="admin", help="DBのユーザー名"
        )
        self.add_argument(
            "-dpass",
            "--db-password",
            default="password",
            help="DBのパスワード",
        )
        self.add_argument(
            "-dd",
            "--db-database",
            default="nanato12_linebot",
            help="DBのデータベース名",
        )
        self.add_argument(
            "-dc", "--db-charset", default="utf8mb4", help="DBの文字コード"
        )

        self.__parse()

    def __parse(self) -> None:
        args = self.parse_args()

        if args.config_name:
            self.__parse_by_config(args.config_name)

        for arg in vars(args).keys():
            v = getattr(args, arg)
            if v is not None:
                setattr(self, arg, v)

        for var in self.class_vars.keys():
            if var in ["token"]:
                continue
            if getattr(self, var) == "":
                raise Exception(f"'{var}' argument variable not set.")

    def __parse_by_config(self, config_name: str) -> None:
        config = get_config_by_name(config_name)

        for var, t in self.class_vars.items():
            if isinstance(v := config.get(var), t) and v:
                setattr(self, var, v)

    @property
    def class_vars(self) -> dict[str, type]:
        return vars(self.__class__).get("__annotations__", {})
