from ormx import Database
from ormx.models import (
    Table,
    Column, ForeignKey
)

db = Database("data.db")


class Author(Table):
    name = Column(str, default='name')
    age = Column(int, default=15)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Post(Table):
    __tablename__ = 'posts'
    title = Column(str)
    draft = Column(bool, default=True)
    author = ForeignKey(Author)


# db.create(Author)
# db.create(Post)
# #


# author = Post(title='Test', draft=False)
#
# db.save(author)


#


test_post = db.get(Post, author_id=1)
#
#

print(test_post)
