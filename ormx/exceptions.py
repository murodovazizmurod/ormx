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


class TableTypeInvalid(TypeError):
    """
    Config not found
    """
    def __init__(self, table):
        if len(f"{type(table)}".split("'")[1].split('.')) > 1:
            self.table = f"{type(table)}".split("'")[1].split('.')[1]
        else:
            self.table = f"{type(table)}".split("'")[1]

    def __str__(self):
        return f"argument must be type 'Table', not {self.table}"


__all__ = [
    "TableInfoError",
    "ConfigKeyNotFound",
    "TableTypeInvalid"
]
