from __future__ import annotations

from dataclasses import dataclass
from string import ascii_lowercase, ascii_uppercase, digits
from typing import ClassVar, List

from linebot.models.emojis import Emoji

HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
HIRAGANA_KOMOJI = "ぁぃぅぇぉっゃゅょ"
HIRAGANA_DAKUON = "がぎぐげござじずぜぞだぢづでどばびぶべぼ"
HIRAGANA_HANDAKUON = "ぱぴぷぺぽ"
KATAKANA = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
KATAKANA_KOMOJI = "ァィゥェォッャュョ"
KATAKANA_DAKUON = "ガギグゲゴザジズゼゾダヂヅデドバビブベボ"
KATAKANA_HANDAKUON = "パピプペポ"
HIRAGANA_OTHER = "ー"
PUNCTUATION = "〜！？@#$%^&*()+/×=[]|;:,./<>-ー¥/「」、…♡♪↑↓→←○〒🔔🍒🍉🍇"

RESOURCE = list(
    HIRAGANA
    + HIRAGANA_KOMOJI
    + HIRAGANA_DAKUON
    + HIRAGANA_HANDAKUON
    + KATAKANA
    + KATAKANA_KOMOJI
    + KATAKANA_DAKUON
    + KATAKANA_HANDAKUON
    + HIRAGANA_OTHER
    + ascii_uppercase
    + ascii_lowercase
    + digits[1:]
    + digits[0]
    + PUNCTUATION
)


@dataclass
class SlotEmoji(Emoji):
    product_id: ClassVar[str] = "620c669d4b44607037707fa1"
    version: ClassVar[int] = 2
    resource_type: ClassVar[str] = "ANIMATION"
    resource: ClassVar[List[str]] = RESOURCE
