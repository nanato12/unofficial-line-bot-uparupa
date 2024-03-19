from dataclasses import dataclass
from typing import Any

from database.models.user import User
from linebot.flex import BaseFlex
from linebot.helpers.calculation import calc_need_exp


@dataclass
class ProfileFlex(BaseFlex):
    user: User

    __alt_text__ = "Profile Flex Message"

    def build(self) -> dict[str, Any]:
        content = self.get_flex_content()
        u: User = self.user

        profile_content = content["contents"][0]["body"]["contents"][0][
            "contents"
        ]

        # icon
        if u.profile_url:
            profile_content[0]["contents"][0]["url"] = u.profile_url

        # name
        profile_content[1]["contents"][0]["contents"][0]["contents"][0][
            "text"
        ] = u.name

        # level
        profile_content[1]["contents"][1]["contents"][0]["contents"][0][
            "contents"
        ][0]["contents"][1]["text"] = str(u.level)

        # exp
        profile_content[1]["contents"][1]["contents"][0]["contents"][1][
            "contents"
        ][0]["contents"][1]["text"] = f"{u.exp:,}"

        # need exp
        profile_content[1]["contents"][1]["contents"][0]["contents"][1][
            "contents"
        ][0]["contents"][3][
            "text"
        ] = f"{calc_need_exp(u.level):,}"  # type: ignore

        return content
