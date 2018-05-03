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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    return redirect('/login')

@app.route('/new_post', methods=['GET', 'POST'])
def add_entry():

    username = User.query.filter_by(username=username).first()
    

    if request.method == 'GET':
        return render_template('new_post.html')

    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['body']
        user_id = request.form['user_id']
        title_error = ""
        body_error = ""
        user_error = ""

        if len(title)< 3:
            title_error = "You need a longer title"

        if len(blog)<3:
            body_error = "You need to write a longer post"

        if not title_error and not body_error:
            new_blog = Blog(title, blog)
            db.session.add(new_blog)
            db.session.commit()
            query_url = "/blog?id=" + str(new_blog.id)
            return redirect(query_url)

        else:
            return render_template('new_post.html', 
            title_error=title_error, body_error=body_error)

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        username = ""
        password = ""
        verify = ""

        if len(username) < 3 or len(username) > 20 or " " in username:
            username_error = 'Not a valid username'

        if len(password) < 3 or len(password) > 20 or " " in password:
            pwd_error = 'Please enter a password between 3 and 20 characters.'

        if verify is "":
            pwdval_error = "Enter a valid password."
    
        elif verify != password:
            pwdval_error = 'Passwords do not match.'

        if not username_error and not pwd_error and not pwdval_error:
            return render_template('blog.html', username=username)
        else:
            return render_template('signup.html', username=username, username_error=username_error, pwd_error=pwd_error, 
            pwdval_error=pwdval_error)

        
@app.route('/signup', methods = ['POST', 'GET'])
def signup():

    existing_user = User.querry.filter_by(username=username).first()
    
    if not existing_user:
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/')

    else:
        
        # user better response message

        return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login.html')

@app.route('/blog', methods = ['GET'])
def index():
    owner = User.query.filter_by(username=session['username']).first()
        
    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)
        db.session.add(blog)
        db.session.commit()

        return render_template('entry.html', blog=blog)

    else:
        blogs = Blog.query.all()

        return render_template('blog.html', blogs=blogs)


if __name__ == '__main__':
    app.run()