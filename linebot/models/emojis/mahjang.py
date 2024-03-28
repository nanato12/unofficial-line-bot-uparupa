from __future__ import annotations

from dataclasses import dataclass
from string import digits
from typing import ClassVar, List

from linebot.models.emojis import Emoji


def get_mahjang_name(type: str) -> List[str]:
    return [f"{d}{type}" for d in digits[1:]]


MANZU = get_mahjang_name("m")
PINZU = get_mahjang_name("p")
SOZU = get_mahjang_name("s")
JIHAI = list("東南西北白發中")
PAI = SOZU + PINZU + MANZU + JIHAI
TENBO = "1000 5000 300 10000".split()
OTHER = "ロン ツモ".split()


@dataclass
class MahjangMUPEmoji(Emoji):
    product_id: ClassVar[str] = "5bfc05cf031a673ca7ee46b4"
    version: ClassVar[int] = 4
    resource_type: ClassVar[str] = "STATIC"
    resource: ClassVar[List[str]] = PAI + TENBO + OTHER
