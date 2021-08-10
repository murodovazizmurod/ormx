from typing import Any

from ormx.exceptions import ConfigKeyNotFound

defaults = {
        "testing": False
}


class Config:
    def __init__(self):
        self.values: dict = defaults

    def __getitem__(self, item):
        if not item in self.values:
            raise ConfigKeyNotFound("Config not found")

        return self.values[item]

    def set(self, config: str, value: Any) -> None:
        if not config in self.values:
            raise ConfigKeyNotFound("Config not found")

        self.values[config] = value


__all__ = [
    "Config"
]