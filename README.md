<div align="center">

<img src="./assets/logo.png" width="300px" alt="ORMX">

# ORMX v 0.1


<br>
<h1><i>Sorry for awful code </i>😅</h1>
</div>
<br>

## Installation
```shell
pip install ormx
```
<br>
<br>
<br>

## Status


| Version |  Status |    Tests, and actions |
| :--------: | :----------------------------: | :---: |
| `0.1`  | ⚠️ unstable          <br> ❌️ first version      |  ~  |


```python
from ormx import Database
from ormx.models import Table, Column, ForeignKey

# Create reference to SQLite database file
db = Database("data.db")

# Define tables
class Author(Table):
    name = Column(str)
    age = Column(int)

class Post(Table):
    title = Column(str)
    draft = Column(bool)
    author = ForeignKey(Author)

# Create tables
db.create(Author)
db.create(Post)

# Create and save an Author in the database
john = Author(name="John Cena", 
              age=44)
db.save(john)

# Fetch all Authors from the database
authors = db.all(Author)

# Fetch a specific Author from the database by ID
user = db.get(Author, 1)

# Create object with reference to another object
post = Post(title="Restling",
            draft=False,
            author=user)

# Save object with foreign key reference
db.save(post)

# Fetching an object with a foreign key
# will dereference that key
print(db.get(Author, 1)) # -> Author.name => 'John Cena'
```


## In progress ...