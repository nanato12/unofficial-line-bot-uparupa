from enum import IntEnum
from typing import Tuple


class Authority(IntEnum):
    NORMAL = 1
    FRIEND = 2
    ADMIN = 999

    @property
    def flex_colors(self) -> Tuple[str, str]:
        match self:
            case Authority.NORMAL:
                return ("#FD6E6A", "#FD6E6A")
            case Authority.FRIEND:
                return ("#FFAA85", "#B3315F")
            case Authority.ADMIN:
                return ("#3C8CE7", "#00EAFF")
            case _:
                raise ValueError(f"Invalid Authority: {self.name}")
