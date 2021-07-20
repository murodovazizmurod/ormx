import sqlite3


from .models import *
from .constants import *


class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def _execute(self, sql, params=None):
        try:
            if params:
                return self.conn.execute(sql, params)
            return self.conn.execute(sql)
        except sqlite3.OperationalError as e:
            print(e)

    @property
    def tables(self):
        return [x[0] for x in self._execute(SELECT_TABLES_SQL).fetchall()]

    def create(self, table):
        self._execute(table._get_create_sql())

    def save(self, instance):
        sql, values = instance._get_insert_sql()
        cursor = self._execute(sql, values)
        instance._data['id'] = cursor.lastrowid
        self.conn.commit()

    def all(self, table):
        sql, fields = table._get_select_all_sql()
        result = []
        for row in self._execute(sql).fetchall():
            new_fields, row = self._dereference(table, fields, row)
            data = dict(zip(new_fields, row))
            result.append(table(**data))
        return result

    def get(self, table, id):
        sql, fields, params = table._get_select_where_sql(id=id)
        row = self._execute(sql, params).fetchone()
        fields, row = self._dereference(table, fields, row)
        row = ['' if b is None else b for b in row]
        data = dict(zip(fields, row))
        return table(**data)

    def _dereference(self, table, fields, row):
        new_fields = []
        new_values = []
        for field, value in zip(fields, row):
            if field.endswith('_id'):
                # strip off "_id" to find field name
                field = field[:-3]
                fk = getattr(table, field)
                # fetch object with the given ID
                value = self.get(fk.table, value)
            new_fields.append(field)
            new_values.append(value)
        return new_fields, new_values


__all__ = [Database]
