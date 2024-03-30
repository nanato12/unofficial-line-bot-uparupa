from datetime import datetime
from typing import Any, Callable, Optional

from CHRLINE.hooks import HooksTracer

from constants.enums.authority import Authority
from database.models.user import User
from linebot.models.command_help import CommandHelp
from repository.user_repository import get_or_create_user_from_mid


class HooksTracerWrapper(HooksTracer):
    setup_timestamp: datetime = datetime.now()

    def getPermission(self, permission: str) -> list[str]:
        return [
            u.mid
            for u in User.query.filter(
                User.authority == Authority(int(permission))
            )
        ]

    def addPermission(self, mid: str, permission: Authority) -> bool:
        authority = Authority(int(permission))
        u = get_or_create_user_from_mid(mid, self.cl)
        if u.authority == authority:
            return False
        u.authority = authority
        u.save()
        return True

    def change_permission(self, mid: str, permission: Authority) -> bool:
        return self.addPermission(mid, permission)

    def genHelp(
        self,
        prefix: Optional[str] = None,
        user_mid: Optional[str] = None,
        msg: Any = None,
    ) -> str:
        return "\n\n".join(
            [h.build_message() for h in self.generate_command_helps()]
        )

    def generate_command_helps(self) -> list[CommandHelp]:
        return [self.gen_function_help(f) for f in self.cmdFuncs]

    def gen_function_help(self, func: Callable[[Any], Any]) -> CommandHelp:
        prefix = self.prefixes[0] if self.prefixes and func.prefixes else ""  # type: ignore [attr-defined]
        if doc := func.__doc__:
            lines = [line.strip() for line in doc.strip().split("\n")]
        else:
            lines = []
        return CommandHelp(prefix, [func.__name__] + func.alt, lines)  # type: ignore [attr-defined]
