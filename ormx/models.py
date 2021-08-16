import inspect
from typing import List

from ormx.constants import *
from ormx.exceptions import *
from ormx.types import *


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

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self._data:
            self._data[key] = value

    @classmethod
    def _get_name(cls):
        return cls.__tablename__.split()[0] if hasattr(cls, '__tablename__') else cls.__name__.lower()

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
        return CREATE_TABLE_SQL.format(
            name=cls.__tablename__.split()[0] if hasattr(cls, '__tablename__') else cls._get_name(),
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

        sql = INSERT_SQL.format(name=cls.__tablename__.split()[0] if hasattr(cls, '__tablename__') else cls._get_name(),
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

    def _get_update_sql(self):
        cls = self.__class__
        fields = []
        values = []

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
                values.append(getattr(self, name))
            elif isinstance(field, ForeignKey):
                fields.append(name + "_id")
                values.append(getattr(self, name).id)

        values.append(getattr(self, 'id'))

        sql = UPDATE_SQL.format(
            name=cls.__name__.lower(),
            fields=', '.join([f"{field} = ?" for field in fields])
        )

        return sql, values

    @classmethod
    def _get_select_all_sql(cls,
                            order_by: tuple,
                            limit: list = None,
                            where: list = None
                            ):
        params = []
        fields = cls._get_column_names()
        sql = SELECT_ALL_SQL.format(name=cls._get_name(),
                                    fields=", ".join(fields))

        if where:
            if isinstance(where[0], str):
                if where[1] in WHERE_OPTS:
                    sql += f' WHERE {where[0]} {where[1]} ?'
                    params.append(where[2])
            elif isinstance(where[0], tuple):
                filters = []
                sql += ' WHERE '
                for i in where:
                    if i[1] in WHERE_OPTS:
                        filters.append(f"{i[0]} {i[1]} ?")
                        params.append(i[2])
                    else:
                        raise TypeError(
                            f"Second parameter in list is wrong, it must be one of: {', '.join(WHERE_OPTS)}")
                sql += f" AND ".join(filters)

            else:
                raise WhereTypeError(where[0])

        if order_by:
            if not isinstance(order_by, tuple):
                raise OrderByParamError(order_by)
            if not (isinstance(order_by[0], str) and order_by[0] in fields):
                raise OrderByColumnError(order_by[0])
            if not (order_by[1] in ORDER_BY_PARAMS):
                raise SortingTypeError(order_by[1])
            sql += f' ORDER BY {order_by[0]} {order_by[1]}'
        if limit:
            if isinstance(limit, list):
                for i in limit:
                    if not isinstance(i, int): raise TypeError(
                        f"Parameters must be int, not {type(i).__name__}")
                if len(limit) == 1:
                    sql += f' LIMIT {limit[0]}'
                elif len(limit) == 2:
                    sql += f' LIMIT {limit[0]} OFFSET {limit[1]}'
                else:
                    raise LimitTooMuchParamsError(limit)

        return sql, fields, tuple(params)

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
    def _get_drop_sql(cls, exp=None):
        sql = DROP_SQL.format(name=cls._get_name(), exp=IF_EXISTS if exp else '')

        return sql

    @classmethod
    def _get_select_where_sql(cls, fields: list = None, **kwargs):
        fields = fields or cls._get_column_names()
        # print(kwargs)

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
        print(locals())

    @property
    def sql_type(self):
        return SQLITE_TYPE_MAP[self.type]

    def __eq__(self, other):
        return f"{locals()}"

    def __ne__(self, other):
        return other, self.__class__.__name__


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
