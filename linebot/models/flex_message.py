from dataclasses import dataclass, field
from typing import Any


@dataclass
class FlexMessage:
    alt_text: str = "flex message"
    contents: dict[str, Any] = field(default_factory=dict)

    def build(self) -> dict[str, Any]:
        return {
            "type": "flex",
            "altText": self.alt_text,
            "contents": self.contents,
        }
