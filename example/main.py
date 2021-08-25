import datetime

from flask import Flask, render_template, request, url_for, redirect

from ormx import Database
from ormx.models import Table, Column

app = Flask(__name__)
db = Database('example/flask.db')


# Models
class Post(Table):
    title = Column(str)
    text = Column(str)
    published = Column(str)


db.create(Post)


# or
# db.create_all([Post])


@app.route('/')
def index():
    try:
        posts = db.all(Post)
    except Exception:
        posts = []
    return render_template('index.html', posts=posts[::-1])


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        if title and text:
            post = Post(title=title, text=text, published=datetime.datetime.now().strftime('%d-%m-%Y %H:%M'))
            db.save(post)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    if request.method == 'GET':
        post = db.get(Post, id=id)

        if post:
            db.delete(post)

        return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        post = db.get(Post, id=id)

        return render_template('update.html', post=post)
    elif request.method == 'POST':
        post = db.get(Post, id=id)
        title = request.form['title']
        text = request.form['text']

        if title and text:
            post.title = title
            post.text = text
            db.update(post)

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
