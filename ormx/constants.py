SELECT_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type = 'table';"
CREATE_TABLE_SQL = "CREATE TABLE {name} ({fields});"
INSERT_SQL = 'INSERT INTO {name} ({fields}) VALUES ({placeholders});'
SELECT_ALL_SQL = 'SELECT {fields} FROM {name};'
SELECT_FIRST_SQL = 'SELECT * FROM {name} ORDER BY ROWID DESC LIMIT 1;'
SELECT_WHERE_SQL = 'SELECT {fields} FROM {name} WHERE {query};'
DELETE_SQL = 'DELETE FROM {name} WHERE {query};'
DROP_SQL = 'DROP TABLE {exp} {name};'
UPDATE_SQL = 'UPDATE {name} SET {fields} WHERE id = ?'

SQLITE_TYPE_MAP = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    bytes: "BLOB",
    bool: "INTEGER",  # 0 or 1
}

IF_EXISTS = "IF EXISTS"

__all__ = [
    "SELECT_TABLES_SQL",
    "CREATE_TABLE_SQL",
    "INSERT_SQL",
    "SELECT_ALL_SQL",
    "SELECT_FIRST_SQL",
    "SELECT_WHERE_SQL",
    "SQLITE_TYPE_MAP",
    "DELETE_SQL",
    "DROP_SQL",
    "IF_EXISTS"
]