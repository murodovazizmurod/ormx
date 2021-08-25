from ormx import Database
from ormx.models import (
    Table,
    Column
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

# db.create(Author)
# db.create(Post)
# #
# db.save(Author(name="Linus", age=99))
#
# db.save(Post(title="Programming",
#              draft=False,
#              author=db.get(Author, id=1)))
# #


test_post = db.get(Post, title="Programming")
#
#
test_author = db.all(Post, where=[
                        ('title', 'LIKE', "Programming"), AND,
                        ('draft', '!=', 1), OR, ('draft', '!=', 1)
                    ],
                     limit=[2],
                     )
