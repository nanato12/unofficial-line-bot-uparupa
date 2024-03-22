from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Union

from more_itertools import chunked

from database.models.user import User
from linebot.flex import BaseFlex
from linebot.logger import get_file_path_logger

logger = get_file_path_logger(__name__)


@dataclass
class RankingFlex(BaseFlex):
    users: list[User] = field(default_factory=list)
    title: str = field(default="全体ランキング")

    __alt_text__ = "Ranking Flex Message"

    def build(self) -> dict[str, Any]:
        content: dict[str, Union[list, Any]] = self.get_flex_content()

        # ranking
        content["contents"][0]["header"]["contents"][0]["text"] = self.title

        base_bubble: dict[str, Union[Any, dict[str, list]]] = content[
            "contents"
        ].pop()
        base_box: dict[str, Any] = base_bubble["body"]["contents"].pop()

        for i, users in enumerate(chunked(self.users, 5)):
            bubble = deepcopy(base_bubble)
            for j, user in enumerate(users, start=1):
                box = deepcopy(base_box)

                box["contents"][0]["contents"][0]["text"] = str(5 * i + j)
                box["contents"][1]["contents"][0]["url"] = user.profile_url
                box["contents"][2]["contents"][0]["contents"][0][
                    "text"
                ] = user.name

                text_box = box["contents"][2]["contents"][1]["contents"][0][
                    "contents"
                ]
                text_box[1]["text"] = str(user.level)
                text_box[3]["text"] = str(user.exp)

                bubble["body"]["contents"].append(box)
            content["contents"].append(bubble)

        return content
