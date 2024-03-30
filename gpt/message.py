from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str

    def build(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}
