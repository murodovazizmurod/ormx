import inspect

from ..constants import *


class Table:

    def __init__(self, **kwargs):
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
    def _get_select_all_sql(cls):
        fields = ['id']
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
            if isinstance(field, ForeignKey):
                fields.append(name + "_id")

        sql = SELECT_ALL_SQL.format(name=cls._get_name(),
                                    fields=", ".join(fields))

        return sql, fields

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
        return sql, fields, params


class Column:

    def __init__(self, type):
        self.type = type

    @property
    def sql_type(self):
        return SQLITE_TYPE_MAP[self.type]


class ForeignKey:

    def __init__(self, table):
        self.table = table