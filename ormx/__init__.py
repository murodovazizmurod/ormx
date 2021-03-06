import logging
from sqlite3 import *
from typing import (
    List,
    Union,
    Tuple,
    AnyStr, Type
)

from prettytable import PrettyTable

from .config import *
from .constants import *
from .exceptions import *
from .models import *
from .models import Table
from .testing import *

logging.basicConfig(format='%(asctime)s - INFO - %(message)s', level=logging.INFO)


__version__ = '0.1.4.12'
__author__ = 'Murodov Azizmurod'


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
        self.conn = connect(path, check_same_thread=False, detect_types=PARSE_DECLTYPES)
        self.cur = self.conn.cursor()
        self.config = Config()

    def __new__(cls, *args, **kwargs):
        instance = super(Database, cls).__new__(cls)
        logging.info('Database connected!')
        return instance

    def __getitem__(self, key) -> ListQuery:
        return ListQuery(key, self)

    def _execute(self, sql: str, params: AnyStr = None) -> Cursor:
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
        except OperationalError as e:
            print(e)

    @property
    def tables(self) -> List:
        return [x[0] for x in self._execute(SELECT_TABLES_SQL).fetchall()]

    def create(self, table: Table) -> None:
        """
        Creates table scheme
        :params
            table: Table Object
        :return:
            List or AnyStr
        """
        self._execute(table._get_create_sql())

    def drop(self, table: Type[Table], if_exists=False) -> None:
        sql = table._get_drop_sql(exp=if_exists)
        self._execute(sql)
        self.conn.commit()

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

    def all(self, table: Table,
            order_by: tuple = None,
            limit: list = None,
            where: list = None,
            fields: list = None,
            pretty_table: bool = False) -> List[Table]:
        """
        Returns all rows from `table`
        :params
            table: Table Object that will used
            order_by: name of column and sorting type. ex. ('title', ASC)
            limit: list of integers. ex. [10, 2] -> LIMIT 10 OFFSET 2
            where: list of filters.
                ex: ['column_name', 'condition', 'value']
                    or
                    [
                        ('name', '==', 'title'),
                        AND,
                        ('draft', '!=', 0),
                        OR
                        ('published', '>=', datetime.now())
                    ]
            fields: list of fields which will be returned. ex. ['title', 'published']
            pretty_table: bool. Printing query with PrettyTable
        :return:
            List of Table Objects
        """
        result = []
        sql, fields, params = table._get_select_all_sql(order_by, limit, where, fields)
        pretty = PrettyTable()
        pretty.field_names = fields
        try:
            for row in self._execute(sql, params).fetchall():
                new_fields, row = self._dereference(table, fields, row)
                data = dict(zip(new_fields, row))
                result.append(table(**data))
                pretty.add_row(list(row))
            result = tuple(result)
            if len(result) == 1: result = result[0]
            return print(pretty) if self.config['testing'] or pretty_table else result
        except AttributeError:
            pass

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

    def get(self, table: Table, fields: list = None, **kwargs) -> Union[Table, tuple, None]:
        """
        Returns row from `table` where ROWID equals `id`
        :params
            table: Table Object that will used
            fields: List - searching fields with value
        :return:
            Table Object
        """
        try:
            sql, fields, params = table._get_select_where_sql(fields=fields, **kwargs)
            result = []
            for row in self._execute(sql, params).fetchall():
                new_fields, row = self._dereference(table, fields, row)
                data = dict(zip(new_fields, row))
                result.append(table(**data))
            if len(result) == 1:
                return result[0]
            elif len(result) == 0:
                return None
            return tuple(result)
        except Exception:
            pass

    def update(self, instance: Table):
        sql, values = instance._get_update_sql()
        self.conn.execute(sql, values)
        self.conn.commit()

    def delete(self, instance: Table):
        if isinstance(instance, Table):
            sql, params = instance._get_delete_sql(id=instance.id)
            self._execute(sql, params)
            self.conn.commit()
        else:
            raise TableTypeInvalid(instance)

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


__all__ = [
    'Database'
]
