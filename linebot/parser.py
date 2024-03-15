import json
from argparse import ArgumentParser
from os.path import exists as path_exists
from typing import Any

from design.singleton import SingletonMeta

DEFAULT_CONFIG_JSON = "config.json"


class ConfigParser(ArgumentParser, metaclass=SingletonMeta):
    config_name: str
    device: str = ""
    token: str = ""
    log_name: str = ""

    def __init__(self) -> None:
        super().__init__()
        self.add_argument(
            "-c", "--config-name", default="default", help="設定名"
        )
        self.add_argument("-d", "--device", help="デバイス名")
        self.add_argument("-t", "--token", help="トークン")
        self.add_argument("-l", "--log-name", help="ログファイル名")
        self.__parse()

    def __parse(self) -> None:
        args = self.parse_args()

        if args.config_name:
            self.__parse_by_config(args.config_name)

        for arg in vars(args).keys():
            v = getattr(args, arg)
            if v is not None:
                setattr(self, arg, v)

    def __parse_by_config(self, config_name: str) -> None:
        config = self.get_config_by_name(config_name)

        self_vars: dict[str, type] = vars(self.__class__).get(
            "__annotations__", {}
        )

        for var, t in self_vars.items():
            if isinstance(v := config.get(var), t) and v:
                setattr(self, var, v)

    @staticmethod
    def get_config_by_name(config_name: str) -> dict[str, Any]:
        if not path_exists(DEFAULT_CONFIG_JSON):
            raise FileNotFoundError(f"'{DEFAULT_CONFIG_JSON}' is not found.")

        with open(DEFAULT_CONFIG_JSON) as f:
            c: dict[str, dict[str, Any]] = json.load(f)
        return c.get(config_name, {})
