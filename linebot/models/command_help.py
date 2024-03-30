from dataclasses import dataclass, field


@dataclass
class CommandHelp:
    prefix: str
    cmds: list[str] = field(default_factory=list)
    lines: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.cmds.sort()

    def build_message(self) -> str:
        cmd = ", ".join([f"{self.prefix}{cmd}" for cmd in self.cmds])
        text = "\n  " + ("\n  ".join(self.lines)) if self.lines else ""
        return f"{cmd}{text}"
