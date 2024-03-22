from typing import Any

from linebot.flex import BaseFlex
from linebot.logger import get_file_path_logger

logger = get_file_path_logger(__name__)


class TestFlex(BaseFlex):

    __alt_text__ = "Test Flex Message"

    def build(self) -> dict[str, Any]:
        content = self.get_flex_content()

        return content
