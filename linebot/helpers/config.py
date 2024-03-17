from json import load as json_load
from os.path import exists as path_exists
from typing import Any

DEFAULT_CONFIG_JSON = "config.json"


def get_config_by_name(config_name: str) -> dict[str, Any]:
    if not path_exists(DEFAULT_CONFIG_JSON):
        raise FileNotFoundError(f"'{DEFAULT_CONFIG_JSON}' is not found.")

    with open(DEFAULT_CONFIG_JSON) as f:
        c: dict[str, dict[str, Any]] = json_load(f)
    return c.get(config_name, {})
