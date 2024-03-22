from os import environ

from linebot.hook.command import common, keyword  # noqa: F401

if environ.get("IS_LOCAL"):
    from linebot.hook.command import develop  # noqa: F401
