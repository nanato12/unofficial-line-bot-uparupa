from linebot.exceptions import UparupaError


class SQLError(UparupaError):
    pass


class NotFoundRecordError(SQLError):
    pass
