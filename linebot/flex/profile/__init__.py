from dataclasses import dataclass
from typing import Any

from database.models.user import User
from linebot.flex import BaseFlex


@dataclass
class ProfileFlex(BaseFlex):
    user: User

    __alt_text__ = "Profile Flex Message"

    def build(self) -> dict[str, Any]:
        content = self.get_flex_content()
        u: User = self.user

        # icon
        content["contents"][0]["body"]["contents"][0]["contents"][0][
            "contents"
        ][0]["url"] = u.profile_url

        # name
        content["contents"][0]["body"]["contents"][0]["contents"][1][
            "contents"
        ][0]["contents"][0]["contents"][0]["text"] = u.name

        return content
