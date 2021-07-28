from ormx import Database
from ormx.models import (
    Table,
    Column,
    Rel
)

db = Database("data.db")


class Author(Table):
    name = Column(str)
    age = Column(int)


class Post(Table):
    title = Column(str)
    draft = Column(bool)

    def __repr__(self):
        return f"{self.title}"


# db.create(Author)
# db.create(Post)
#
# db.save(Author(name="Linus", age=99))
#
# db.save(Post(title="Programming",
#              draft=False,
#              author=db.get(Author, 1)))
#


# test_post = db.get(Post, id=1, title='Programming')
# test_author = db.all(Author)[0]


class User(Table):
    name = Column(str)
    age = Column(int)
    posts = Rel(Post)

    def __repr__(self):
        return f"{self.name}"


# def test_authors():
#     assert len(db.all(Author)) > 0
#
#
# def test_posts():
#     assert len(db.all(Post)) > 0
#
#
# def test_author_name():
#     assert 'Linus' == test_author.name
#
#
# def test_post_title():
#     assert "Programming" == test_post.title
#
#
# def test_post_author():
#     assert "Linus" == test_post.author.name
class Fact(Table):
    name = Column(str)
    posts = Rel(Post)


# db.create(Fact)

db.config.set('testing', True)
# db.save(Fact(name='Fact'))
print(db.all(Author))
