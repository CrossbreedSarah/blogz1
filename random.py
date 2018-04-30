from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:sarah@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body
    
@app.route('/new_post', methods=['GET', 'POST'])
def new_post():    
    if request.method == 'POST':
        title = request.form['blog']
        body = request.form['new_post']
        title = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()

    return render_template('new_post.html', title="Add New Blog Entry", 
    blogs=blogs)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(blog).all()
    new_blog = Blog.query.filter_by(new_blog).all()
        
    return render_template('base.html', title="Build A Blog", 
    Blog=Blog, new_blog=new_blog)

app.run()