from typing import Any

from linebot.flex import BaseFlex


class ProfileFlex(BaseFlex):
    __alt_text__ = "Profile Flex Message"

    def build(self) -> dict[str, Any]:
        return self.get_flex_content()
