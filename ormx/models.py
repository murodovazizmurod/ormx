import inspect
from ormx.constants import DELETE_SQL

from ormx import *
from ormx.exceptions import TableTypeInvalid


class Table:
    """
    Sub-class of Database, itself one table of Database
    Have same methods but without table name argument
    Attributes
    ----------
    name : str
        Name of table
    columns = list
        Generator of columns in table
    columns_names = list
        Generator of column's names in table
    """

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        Keyword Anguments
        """
        self._data = {
            'id': None
        }
        for key, value in kwargs.items():
            self._data[key] = value

    def __getattribute__(self, key):
        _data = object.__getattribute__(self, '_data')
        if key in _data:
            return _data[key]
        return object.__getattribute__(self, key)

    @classmethod
    def _get_name(cls):
        return cls.__name__.lower()

    @classmethod
    def _get_create_sql(cls):
        fields = [
            ("id", "INTEGER PRIMARY KEY AUTOINCREMENT")
        ]

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append((name, field.sql_type))
            elif isinstance(field, ForeignKey):
                fields.append((name + "_id", "INTEGER"))

        fields = [" ".join(x) for x in fields]
        return CREATE_TABLE_SQL.format(name=cls._get_name(),
                                       fields=", ".join(fields))

    @classmethod
    def _get_column_names(cls):
        fields = ['id']
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
            if isinstance(field, ForeignKey):
                fields.append(name + "_id")
        return fields

    def _get_insert_sql(self):
        cls = self.__class__
        fields = []
        placeholders = []
        values = []

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
                values.append(getattr(self, name))
                placeholders.append('?')
            elif isinstance(field, ForeignKey):
                fields.append(name + "_id")
                values.append(getattr(self, name).id)
                placeholders.append('?')

        sql = INSERT_SQL.format(name=cls._get_name(),
                                fields=", ".join(fields),
                                placeholders=", ".join(placeholders))

        return sql, values

    @classmethod
    def _get_first_sql(cls):
        sql = SELECT_FIRST_SQL.format(name=cls._get_name())

        return sql

    @classmethod
    def _get_count_sql(cls):
        sql = SELECT_ALL_SQL.format(fields='COUNT(*)', name=cls._get_name())

        return sql

    @classmethod
    def _get_select_all_sql(cls):
        fields = cls._get_column_names()
        sql = SELECT_ALL_SQL.format(name=cls._get_name(),
                                    fields=", ".join(fields))

        return sql, fields

    @classmethod
    def _rows(cls):
        return inspect.getmembers(cls)

    @classmethod
    def _get_delete_sql(cls, **kwargs):
        filters = []
        params = []
        for key, value in kwargs.items():
            filters.append(key + " = ?")
            params.append(value)
        sql = DELETE_SQL.format(name=cls._get_name(),
                                query=" AND ".join(filters))
        
        return sql, tuple(params)

    @classmethod
    def _get_select_where_sql(cls, **kwargs):
        fields = ['id']
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
            if isinstance(field, ForeignKey):
                fields.append(name + "_id")

        filters = []
        params = []
        for key, value in kwargs.items():
            filters.append(key + " = ?")
            params.append(value)

        sql = SELECT_WHERE_SQL.format(name=cls._get_name(),
                                      fields=", ".join(fields),
                                      query=" AND ".join(filters))
        return sql, fields, tuple(params)

    @classmethod
    def _name(cls):
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        atrs = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
        return atrs


class Column:

    def __init__(self, type):
        self.type = type

    @property
    def sql_type(self):
        return SQLITE_TYPE_MAP[self.type]


class ForeignKey:

    def __init__(self, table):
        self.table = table


class Rel:

    def __init__(self, table):
        self.table = table
        self._data: List[table: Table] = []

    def __str__(self):
        return f"<Relation{self._data}>"

    def add(self, table: Table) -> None:
        if not isinstance(table, self.table):
            raise TableTypeInvalid(table)
        self._data.append(table)


__all__ = [
    'Table',
    'Column',
    'ForeignKey',
    'Rel'
]
