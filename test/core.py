from ormx import Database
from ormx.models import (
    Table,
    Column, ForeignKey
)
from ormx.types import *

db = Database("data.db")


class Author(Table):
    name = Column(str)
    age = Column(int)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Post(Table):
    __tablename__ = 'posts'
    title = Column(str)
    draft = Column(bool)
    author = ForeignKey(Author)

# db.create(Author)
# db.create(Post)
# #
# author = Author(name="Linus", age=99)
# db.save(author)


#


test_post = db.get(Post, author_id=1)
#
#
test_author = db.all(Post, where=['author_id', '==', 1])

print(test_post)