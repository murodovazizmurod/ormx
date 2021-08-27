# **ORMX**

<div align="center">
    <img src="./assets/logo.png" width="300px" alt="ORMX"><br>
    <a href="https://badge.fury.io/py/ormx"><img src="https://badge.fury.io/py/ormx.svg" alt="PyPI version" height="18"></a>
    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/murodovazizmurod/ormx">
    <a href="https://github.com/murodovazizmurod/ormx/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/murodovazizmurod/ormx"></a><br>
    <a href="https://lgtm.com/projects/g/murodovazizmurod/ormx/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/murodovazizmurod/ormx.svg?logo=lgtm&logoWidth=18"/></a>
    <a href="https://lgtm.com/projects/g/murodovazizmurod/ormx/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/murodovazizmurod/ormx.svg?logo=lgtm&logoWidth=18"/></a>
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/murodovazizmurod/ormx">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/murodovazizmurod/ormx"><br>
    <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/murodovazizmurod/ormx">
    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/murodovazizmurod/ormx/total">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/ormx">
    <a href="https://github.com/murodovazizmurod/ormx/blob/main/LICENSE.txt"><img alt="GitHub license" src="https://img.shields.io/github/license/murodovazizmurod/ormx"></a>
</div>

<hr>

```bash
$ pip install ormx
```

## Status

| Version | Status                  | Tests and Actions |
| ------- | ----------------------- | ----------------- |
| `0.1.4.12`   | unstable, first version | ~                 |

# **Usage**📖

> Now, `ORMX` supports only `SQLITE` databases😁

## Connecting database🔌

By importing Database class you can establish a new connection:

```python
from ormx import Database

db = Database(database_file:str)
```

<hr>

### Properties
`tables` - returns list of table names in database<br>
```python
tables(Database) -> List
```
Example:
```python
>> db.tables

# ['posts', 'author']
```

<hr>

## Defining Tables ✏

You should import Table, Column from `ormx.models`:

```python
from ormx.models import (
    Table,
    Column
)
```

Create any class by naming your table with including `Table` class:

```python
class User(Table):
    __tablename__ = 'users'
    name = Column(str)
    age = Column(int)
```
<b>
In this code, our table is named as `user` and columns of the table are named as `name` and `age`.

Types:

- `str` - string('Linus'...),
- `int` - integer(1,2,3 ...),
- `bool` - boolean(True, False) or 1,0
- `bytes` - bytes, blob
- `float` - 3.15 ...
- `datetime` - datetime object
</b>
  
`Example:`
```python
class User(Table):
    __tablename__ = 'users'
    name = Column(str)
    age = Column(int)
    registered_at = Column(datetime)
    online = Column(bool)

    def __repr__(self):
        return f"{self.name}"


db.create(User)

user = User(name='User', age=15, date=datetime.now())

db.save(user)

user = db.get(User, id=1)

print(type(user.name)) # <class 'str'>
print(type(user.age)) # <class 'int'>
print(type(user.date)) # <class 'datetime.datetime'>
print(type(user.online)) # <class 'bool'>
```

<b>New Feature</b>
Now you can add default values for each column.

`Example:`

```python
class Post(Table):
    __tablename__ = 'posts'
    title = Column(str, 'some title')
    draft = Column(bool, default=True)
```

<hr>

## Creating Tables🎉

```python
# db : Database
db.create(TABLE:Table)

"""
* TABLE - your class in which you defined your table
"""

db.create(User)
# or
# db.create(User, Post)
```

<hr>

## Drop Table

```python
# db : Database

db.drop(User)

# You can add arguments such as `if_exists`
# db.drop(User, if_exists=True) -> SQL request: `DROP TABLE IF EXISTS table_name`
```

<hr>

## Configuration

### Default values
```python
{
    "testing": False
}
```

<b>Get value</b>
```python
db.config[value]
```
<b>Example</b>
```python
>> db.config['testing'] # -> False
```
<b>Set value</b>
```python
db.config.set(key, value)
```

<b>Example</b>

```python
# Testing mode
>> db.config.set('testing', True)
```
<hr>

## Simple Relationships✨

> `Foreign Key`

Example:

```python
class Post(Table):
    title = Column(str)
    draft = Column(bool)
    author = ForeignKey(User)
```

<b>
Columns:

- title - string
- draft - boolean
- author - belongs to the `User` class in the example presented on the top.
</b>

```python
# Create all tables

db.create(User)
db.create(Post)
```

# Creating and Selecting Objects🕹

<b>Creating and selecting objects similar to other ORMs:</b>

> `Database.save()`

```python
user = User(name="Linus",age=44)
db.save(user)
```

> For saving objects you should write db.save(object)

<hr>

<b>For fetching all data:</b>

```python
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
```

```python
users = db.all(User)
```
<b>or</b>
```python
users = db['user']
```

<i>`PrettyTable` usage:</i>

```python
users = db.all(User, pretty_table=True)

# +----+-----+-------+
# | id | age |  name |
# +----+-----+-------+
# | 1  |  99 | Linus |
# | 2  |  99 | Linus |
# | 3  |  99 | Linus |
# | 4  |  99 | Linus |
# ....

```

<hr>

### <b>Where</b>
Source:
```python
db.all(table: Table, where=['column_name', 'condition', 'value'])
# or
db.all(table: Table, where=[
    ('column_name', 'condition', 'value'),
    ('column_name2', 'condition2', 'value2')
])
```
`SQL code:`
```text
SELECT id, draft, title FROM post WHERE title == ?;
```
<br>

`Example:`
```python
db.all(Post, where=['title', '==', "Programming"])

# or

db.all(Post, where=[('title', '==', "Programming"),
                    ('draft', '>', 0)]
       )

# or

db.all(Post, where=[
             ('title', '==', 'title'),
             AND,
             ('draft', '!=', 0),
             OR,
             ('published', '>=', datetime.now())
             ],
             order_by=['title', DESC]
             limit=[10, 2],
             fields=['title', 'draft']
       )
```

`Conditions: `
```python
[
    "<", "<<", "<=",
    ">=", ">>", ">",
    "=", "==", "!=", "<>",
    "IN", "LIKE"
]
```
Exceptions:

`WhereTypeError` - <b>given wrong type to `where`</b><br><br>

### <b>Order BY</b>
`Example:`

```python
from ormx.types import ASC, DESC

db.all(User, order_by=('name', ASC))

db.all(Post, order_by=('title', DESC))
```

Exceptions:

`OrderByParamError` - <b>order_by parameter must be `tuple`</b><br><br>
`OrderByColumnError` - <b>`column` not exists</b><br><br>
`SortingTypeError` - <b>second element of `order_by` tuple must be `ASC` or `DESC`</b>

<hr>

### <b>Limit Offset</b>
`Code`:
```python
db.all(table: Table, order_by=(column_name, List[ASC, DESC]), limit=List[LIMIT, OFFSET])
```

`Example:`

```python
from ormx.types import DESC

db.all(User, limit=[1]) # -> sql: SELECT id, age, name FROM author LIMIT 1

db.all(User, limit=[10, 1]) # -> sql: SELECT id, age, name FROM author LIMIT 10 OFFSET 1

db.all(User, order_by=('id', DESC), limit=[10, 1]) # -> sql: SELECT id, age, name FROM author ORDER BY id DESC LIMIT 10 OFFSET 1
```

Exceptions:

`LimitTooMuchParamsError` - <b>given too much values in list</b><br><br>


<hr>

<b>Get count of rows in table or count of tables in Database</b>

#### `Source:`
```python
count(self, table: Union[Table] = None) -> int
```
<br/>

```python
db.count(Post) # -> int: count of rows in Post table
```
or
```python
db.count() # -> int: count of tables in database
```
<hr>

<b>Update data</b>

```python
Database.update(self, instance: Table)
```
`Example:`
```python
post = db.get(Post, id=1)

print(post.title) # Old value

post.title = 'New value'

db.update(post)

print(post.title) # New value
```

<hr>

<b>Delete column</b>

```python
author = db.get(Author, id=1)

db.delete(author)
```

Exceptions:

`TableTypeInvalid`

<hr>

<b>For fetching spec. object by their column name</b>

> `Database.get(TABLE:Table, **kwargs)`<br>

`Returns List Object`
<br>

```python
user = db.get(User, id=1, title='C++')
```


<hr>
<b>Fetch last data from table</b>

```python
user = db.first(User)
```

<hr>

<b>Fetching objects in cases of `ForeignKey`:</b>

```python
# Create a simple post with related user:
post = Post(title="C++",draft=False,author=user)

# Save it
db.save(post)

# Fetch it!
fetched = db.get(Post, id=1)

print(fetched.author.name)
# >>> 'Linus'
```

<hr>

## Some Examples:

<b>Flask + ORMX CRUD app: https://ec099b10e8.pythonanywhere.com/ </b>

<b>Photo-Sharing app: https://photo-sharing-ormx.herokuapp.com/ </b>


<b>Article: https://community.uzbekcoders.uz/post/photo-sharing-dasturini-yaratamiz---flask-ormx-cloud-cdn-612787f94f5a32648e01ccc3 </b>

<hr>

**In progress 🔄**
