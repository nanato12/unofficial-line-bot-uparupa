from os import environ

from linebot.hook.command import (  # noqa: F401
    common,
    keyword,
    ranking,
    user_profile,
)

if environ.get("IS_LOCAL"):
    from linebot.hook.command import develop  # noqa: F401
