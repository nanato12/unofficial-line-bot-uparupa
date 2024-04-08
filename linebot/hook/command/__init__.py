from os import environ

from linebot.hook.command import (  # noqa: F401
    admin,
    common,
    emoji,
    enjoyment,
    keyword,
    mention_check,
    message,
    message_read,
    ranking,
    user_profile,
)

if environ.get("IS_LOCAL"):
    from linebot.hook.command import develop  # noqa: F401
