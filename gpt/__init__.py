from dataclasses import dataclass, field

from g4f import ChatCompletion

from gpt.message import Message
from gpt.role import Role


@dataclass
class GPT:
    model: str
    initialize_messages: list[Message] = field(default_factory=list)
    messages: list[Message] = field(init=False, default_factory=list)

    def add_user_message(self, text: str) -> None:
        self.messages.append(Message(Role.USER, text))

    def clear_prompt(self) -> None:
        self.messages = []

    def create(self) -> str:
        return ChatCompletion.create(  # type: ignore [no-any-return]
            model=self.model,
            messages=[
                m.build() for m in self.initialize_messages + self.messages
            ],
        ).strip()
