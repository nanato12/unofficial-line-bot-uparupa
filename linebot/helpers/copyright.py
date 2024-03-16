from datetime import datetime, timedelta, timezone


def get_copyright() -> str:
    now = datetime.now(tz=timezone(timedelta(hours=9)))
    return f"©︎{now.year} nanato12"
