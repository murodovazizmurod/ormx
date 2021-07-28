import sqlite3
from typing import List, Union, AnyStr, Tuple

from .constants import *
from .exceptions import *
from .models import *
from .config import *
from .testing import *


class Database:
    """
    ORMX Database Object
    Attributes
    ----------
    __path : PathType
        Local __str__ to database (PathType)
    """

    def __init__(self, path):
        """
        Initialization
        Parameters
        ----------
        path : PathType
            Local __str__ to database (PathType)
        """
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.config = Config()

    def __getitem__(self, key) -> List:
        if key in self.tables:
            rows = self.cur.execute(f"SELECT * FROM {key}").fetchall()
            fields = [description[0] for description in self.cur.description]
            return [dict(zip(fields, rows[i])) for i in range(len(rows))]
        else:
            raise TableInfoError

    def _execute(self, sql: str, params: AnyStr = None) -> Union[List, None]:
        """
        Execute any SQL-script whit (or without) values, or execute SQLRequest
        Parameters
        ----------
        sql : AnyStr
            single SQLite script, might contains placeholders
        params : AnyStr
            Values for placeholders if script contains it
        Returns
        ----------
        Union[List, None]
            Database answer if it has
        """
        try:
            if params:
                return self.conn.execute(sql, params)
            return self.conn.execute(sql)
        except sqlite3.OperationalError as e:
            print(e)

    @property
    def tables(self) -> List:
        return [x[0] for x in self._execute(SELECT_TABLES_SQL).fetchall()]

    def create(self, table: Table) -> Union[None, AnyStr]:
        """
        Creates table scheme
        :params
            table: Table Object
        :return:
            List or AnyStr
        """
        self._execute(table._get_create_sql())

    def save(self, instance: Table):
        """
        Inserts data to `table`
        :params
            instance: Copy of Table Object
        :return:
            List of Table Objects
        """
        sql, values = instance._get_insert_sql()
        cursor = self._execute(sql, values)
        instance._data['id'] = cursor.lastrowid
        self.conn.commit()

    def all(self, table: Table) -> List[Table]:
        """
        Returns all rows from `table`
        :params
            table: Table Object that will used
        :return:
            List of Table Objects
        """
        sql, fields = table._get_select_all_sql()
        result = []
        for row in self._execute(sql).fetchall():
            new_fields, row = self._dereference(table, fields, row)
            data = dict(zip(new_fields, row))
            result.append(table(**data))
        return result

    def first(self, table: Union[Table]) -> Table:
        """
        Returns first row from `table`
        :params
            table: Table Object that will used
        :return:
            Table Object
        """
        sql, fields = table._get_first_sql(), table._get_column_names()
        row = self._execute(sql).fetchone()
        fields, row = self._dereference(table, fields, row)
        data = dict(zip(fields, row))
        return table(**data)

    def count(self, table: Union[Table] = None) -> int:
        """
        Returns first row from `table`
        :params
            table: Table Object that will used
            type: Type of quering data
        :return:
            int: Number of row in column or tables
        """
        if table:
            sql = table._get_count_sql()
            row = int(self._execute(sql).fetchone()[0])
            return row
        else:
            return len(self.tables)

    def get(self, table: Table, **kwargs) -> Union[Table, Tuple]:
        """
        Returns row from `table` where ROWID equals `id`
        :params
            table: Table Object that will used
            id: Integer - ROWID
        :return:
            Table Object
        """
        sql, fields, params = table._get_select_where_sql(**kwargs)
        result = []
        for row in self._execute(sql, params).fetchall():
            new_fields, row = self._dereference(table, fields, row)
            data = dict(zip(new_fields, row))
            result.append(table(**data))
        if len(result) == 1:
            return result[0]
        return tuple(result)

    def _dereference(self, table: Table, fields: List, row: Union[List, Tuple]) -> Tuple:
        new_fields = []
        new_values = []
        for field, value in zip(fields, row):
            if field.endswith('_id'):
                # strip off "_id" to find field name
                field = field[:-3]
                fk = getattr(table, field)
                # # fetch object with the given ID
                value = self.get(fk.table, id=value)
            new_fields.append(field)
            new_values.append(value)
        return new_fields, new_values

