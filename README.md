# **ORMX**

<div align="center">
    <img src="./assets/logo.png" width="300px" alt="ORMX"><br>
    <a href="https://badge.fury.io/py/ormx"><img src="https://badge.fury.io/py/ormx.svg" alt="PyPI version" height="18"></a>
</div>

<hr>

```bash
$ pip install ormx
```

## Status

| Version | Status                  | Tests and Actions |
| ------- | ----------------------- | ----------------- |
| `0.1`   | unstable, first version | ~                 |

# **Usage**📖

> Now, `ORMX` supports only `SQLITE` databases😁

## Connecting database🔌

By importing Database class you can establish a new connection:

```python
from ormx import Database

db = Database(database_file:str)
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
    name = Column(str)
    age = Column(int)
```

In this code, our table is named as `user` and columns of the table are named as `name` and `age`.

Types:

- `str` - string('Linus'...),
- `int` - integer(1,2,3 ...),
- `bool` - boolean(True, False)

<hr>

## Creating Tables🎉

```python
# db : Database
db.create(TABLE:Table)

"""
* TABLE - your class in which you defined your table
"""

db.create(User)
```

<hr>

## Simple Relationships✨

> Foreign Key

Example:

```python
class Post(Table):
    title = Column(str)
    draft = Column(bool)
    author = ForeignKey(User)
```

Columns:

- title - string
- draft - boolean
- author - belongs to the `User` class in the example presented on the top.

```python
# Create all tables

db.create(User)
db.create(Post)
```

# Creating and Selecting Objects🕹

Creating and selecting objects similar to other ORMs:

> `Database.save()`

```python
user = User(name="Linus",age=44)
db.save(user)
```

> For saving objects you should write db.save(object)

<hr>

For fetching all data:

> `Database.all(Table)`

```python
users = db.all(User)
```

<hr>

For fetching spec. object by their id

> `Database.get(TABLE:Table, id:int)`

```python
user = db.get(User, 1)
```

<hr>

Fetching objects in cases of `ForeignKey`:

```python
# Create a simple post with related user:
post = Post(title="C++",draft=False,author=user)

# Save it
db.save(post)

# Fetch it!
fetched = db.get(Post,1)

print(fetched.author.name)
# >>> 'Linus'
```

<hr>

**In progress 🔄**
