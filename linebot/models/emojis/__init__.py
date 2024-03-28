from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Tuple


@dataclass
class Emoji(ABC):
    text: str
    sticon_id: str
    start: int = 0
    end: int = 0
    product_id: ClassVar[str] = ""
    version: ClassVar[int] = 0
    resource_type: ClassVar[str] = ""
    resource: ClassVar[List[str]] = field(init=False, repr=False)

    def to_resource_data(self) -> Dict[str, Any]:
        return {
            "S": self.start,
            "E": self.end,
            "productId": self.product_id,
            "sticonId": self.sticon_id,
            "version": self.version,
            "resourceType": self.resource_type,
        }

    @classmethod
    def from_char(cls, c: str) -> Emoji:
        if c not in cls.resource:
            raise ValueError(f"'{c}' not in {cls.resource}")
        return cls(text=c, sticon_id=f"{cls.resource.index(c)+1:03d}")

    @classmethod
    def all(cls) -> List[Emoji]:
        return [
            cls(text=v, sticon_id=f"{i:03d}")
            for i, v in enumerate(cls.resource, start=1)
        ]

    @classmethod
    def convert_message(cls, texts: List[str]) -> Tuple[str, List[Emoji]]:
        text = ""
        emojis: List[Emoji] = []

        for c in texts:
            try:
                emoji = cls.from_char(c)
                emoji.start = len(text)
                text += f"({c})"
                emoji.end = len(text)
                emojis.append(emoji)
            except ValueError:
                text += c
        return text, emojis
