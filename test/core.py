from ormx import Database
from ormx.models import (
    Table,
    Column,
    Rel
)


db = Database("data.db")


# class Author(Table):
#     name = Column(str)
#     age = Column(int)


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


test_post = db.get(Post, id=1, title='Programming')
# test_author = db.get(Author, id=1)


class User(Table):
    name = Column(str)
    age = Column(int)
    posts = Rel(Post)

    def __repr__(self):
        return f"{self.name}"


# db.create(User)

User.posts.data.append(test_post)

print(User.posts)

# timeit(db.get(Post, draft=False))(db=db)


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



