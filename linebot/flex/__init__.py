from abc import ABC, abstractmethod
from inspect import getfile
from json import load as json_load
from os.path import dirname
from os.path import join as path_join
from typing import Any

from linebot.helpers.copyright import get_copyright
from linebot.models.flex_message import FlexMessage


class BaseFlex(ABC):
    __alt_text__ = "Flex Message"

    def get_flex_content(
        self, file_name: str = "flex.json", footer: bool = True
    ) -> dict[str, Any]:
        with open(path_join(dirname(getfile(self.__class__)), file_name)) as f:
            j: dict[str, Any] = json_load(f)
        if footer:
            footer_content = self.__get_footer_content()
            for bubble in j["contents"]:
                bubble["footer"] = footer_content
        return j

    def build_message(self) -> dict[str, Any]:
        return FlexMessage(self.__alt_text__, contents=self.build()).build()

    @staticmethod
    def __get_footer_content() -> dict[str, Any]:
        with open(path_join(dirname(__file__), "footer.json")) as f:
            j: dict[str, Any] = json_load(f)
            j["contents"][0]["text"] = get_copyright()
        return j

    @abstractmethod
    def build(self) -> dict[str, Any]:
        pass
