SELECT_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type = 'table';"
CREATE_TABLE_SQL = "CREATE TABLE {name} ({fields});"
INSERT_SQL = 'INSERT INTO {name} ({fields}) VALUES ({placeholders});'
SELECT_ALL_SQL = 'SELECT {fields} FROM {name};'
SELECT_WHERE_SQL = 'SELECT {fields} FROM {name} WHERE {query};'

SQLITE_TYPE_MAP = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    bytes: "BLOB",
    bool: "INTEGER",  # 0 or 1
}