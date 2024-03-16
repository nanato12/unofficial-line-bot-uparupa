from typing import Any

from linebot.flex import BaseFlex


class ProfileFlex(BaseFlex):
    def build(self) -> dict[str, Any]:
        return self.get_flex_content()
