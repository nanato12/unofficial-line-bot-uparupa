from typing import Any


class SingletonMeta(type):
    _instances: dict[Any, object] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
