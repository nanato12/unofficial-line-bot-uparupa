from linebot.exceptions import UparupaError


class AuthorizationError(UparupaError):
    pass


class LevelInsufficiencyError(AuthorizationError):
    pass


class ExpInsufficiencyError(AuthorizationError):
    pass
