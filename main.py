from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://build-a-blog:sarah@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods = ['GET'])
def index():

    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)

        return render_template('entry.html', blog=blog)

    else:
        blogs = Blog.query.all()

        return render_template('blog.html', blogs=blogs)

@app.route('/new_post', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'GET':
        return render_template('new_post.html')

    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['body']
        title_error = ""
        body_error = ""

        if len(title)< 1:
            title_error = "You need a longer title"

        if len(blog)<1:
            body_error = "You need to write a longer post"

        if not title_error and not body_error:
            new_blog = Blog(title, blog)
            db.session.add(new_blog)
            db.session.commit()
            query_url = "/blog?id=" + str(new_blog.id)
            return redirect(query_url)

        else:
            return render_template('new_post.html', title_error=title_error, body_error=body_error)

if __name__ == '__main__':
    app.run()