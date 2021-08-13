from ormx.types import ORDER_BY_PARAMS


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
        self.table = type(table).__class__.__name__

    def __str__(self):
        return f"argument must be type 'Table', not {self.table}"


class OrderByParamError(Exception):
    def __init__(self, param):
        self.param = param

    def __str__(self):
        return f"Order by parameter must be tuple, not {type(self.param).__name__}"


class OrderByColumnError(Exception):
    def __init__(self, param):
        self.param = param

    def __str__(self):
        return f"Column {self.param} is not exists"


class SortingTypeError(Exception):
    def __init__(self, param):
        self.param = param

    def __str__(self):
        return f"{self.param} is incorrect sorting type, it must be on of {', '.join([f'`{i}`' for i in ORDER_BY_PARAMS])}"


class LimitTooMuchParamsError(Exception):
    def __init__(self, param):
        self.param = param

    def __str__(self):
        return f"Maximum parameters count must be under 2, given {len(self.param)}"


class WhereTypeError(TypeError):
    def __init__(self, param):
        self.param = type(param).__name__

    def __str__(self):
        return f"Item's type must str or tuple, not {self.param}"


__all__ = [
    "TableInfoError",
    "ConfigKeyNotFound",
    "TableTypeInvalid",
    "OrderByParamError",
    "OrderByColumnError",
    "SortingTypeError",
    "LimitTooMuchParamsError",
    "WhereTypeError"
]
