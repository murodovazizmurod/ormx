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
    return render_template('index.html', posts=posts)

    
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        if title and text:

            post = Post(title=title, text=text)
            db.save(post)
        return redirect(url_for('index'))
    return render_template('add.html')


app.run()
