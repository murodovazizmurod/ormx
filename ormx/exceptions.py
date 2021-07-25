class TableInfoError(MemoryError):
    """
    Table doesn't exist or have no columns
    """

    def __str__(self):
        return "Table doesn't exist or have no columns"


class ConfigKeyNotFound(KeyError):
    """
    Config not found
    """

    def __str__(self):
        return "Config not found"

__all__ = [
    "TableInfoError",
]
