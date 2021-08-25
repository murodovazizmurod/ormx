DESC = 'DESC'
ASC = 'ASC'
AND = 'AND'
OR = 'OR'

ORDER_BY_PARAMS = [
    ASC,
    DESC
]

WHERE_OPTS = [
    "<", "<<", "<=",
    ">=", ">>", ">",
    "=", "==", "!=", "<>",
    "IN", "LIKE"
]

WHERE_CONDITIONS = [
    AND,
    OR
]

__all__ = [
    'DESC',
    'ASC',
    'AND',
    'OR',
    'ORDER_BY_PARAMS',
    'WHERE_OPTS',
    'WHERE_CONDITIONS'
]
