from dataclasses import dataclass
from typing import Any

from database.models.user import User
from linebot.flex import BaseFlex
from linebot.logger import get_file_path_logger

logger = get_file_path_logger(__name__)


@dataclass
class RankingFlex(BaseFlex):
    users: list[User]

    __alt_text__ = "Ranking Flex Message"

    def build(self) -> dict[str, Any]:
        content = self.get_flex_content()

        return content
