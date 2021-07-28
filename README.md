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
<b>
In this code, our table is named as `user` and columns of the table are named as `name` and `age`.

Types:

- `str` - string('Linus'...),
- `int` - integer(1,2,3 ...),
- `bool` - boolean(True, False) or 1,0
- `bytes` - bytes, blob
- `float` - 3.15 ...
</b>
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

```python
db.config.set(key, value)
```

<b>Example</b>

```python
# Testing mode
db.config.set('testing', True)
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

> `Database.all(Table)`

```python
users = db.all(User)
```
<b>or</b>
```python
users = db['user']
```

<hr>

<b>Get count of rows in table or count of tables in Database</b>

```python
db.count(Post) # -> int: count of rows in Post table
```
or
```python
db.count() # -> int: count of tables in database
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
Don't use!!!

<b>One to Many Relation Example</b>

```python
class User(Table):
    name = Column(str)
    age = Column(int)
    posts = Rel(Post)
    
    def __repr__(self):
        return f"{self.name}"

user = User(name='Gvido',
            age=44)

post = db.get(Post, id=1)

db.save(user)

# add data to `posts`
user.posts.data.append(post)

# remove data to `posts`
user.posts.data.remove(post)

# user.posts.data -> List Object
```
<hr>

**In progress 🔄**
