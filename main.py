from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://blog:sarah@localhost:8889/blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'kj4nkj45kjn6jn89'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return str(self.username)

@app.before_request
def require_login():
    allowed_routes = ['login', 'login', 'index', 'blog', 'individual_blog']
    if request.endpoint not in allowed_routes:
        if 'user' not in session:
            return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():

    username = ""
    password = ""
    username_error = ""
    password_error = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first() 
        
        if user and user.password == password:
            session['user'] = user.id
            return redirect("/new_post?id=" + str(user.id))
        if not user or username == ' ':
            username_error = "Please enter a valid username."
            return render_template('login.html', username_error=username_error)
        else:
            password_error = "Please enter a valid password."
            return render_template('/login.html', password_error=password_error, username=username)
        return render_template("login.html", username_error=username_error, password_error=password_error)

    else:
        return render_template("login.html")
        
@app.route('/signup', methods = ['POST', 'GET'])
def register():

    username = ""
    password = ""
    verify = ""
    username_error = ""
    password_error = ""
    verify_error = ""
    #existing_user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        

        if len(username) < 3 or len(username) > 20 or " " in username:
            username_error = 'Not a valid username'
        #elif existing_user:
        #    username_error = "Username already exists"


        if len(password) <3 or len(password) >20 or " " in password:
            password_error = 'Please enter a password between 3 and 20 characters.'

        if verify == ' ' or password != verify:
            verify ==''
            verify_error = "Passwords must match."

        if not username_error and not password_error and not verify_error:
            new_user=User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = new_user.id
            return redirect("/new_post?id=" + str(new_user.id))
        else:
            return render_template('signup.html', username=username,
            username_error=username_error, password_error=password_error, 
            verify_error=verify_error)

    else:
        return render_template("signup.html")

    #if not existing_user:
     #   new_user = User(username, password)
      #  db.session.add(new_user)
      #  db.session.commit()
      #  session['username'] = username
      #  return redirect('/blog')

    #else:
        
    #    return "<h1>Duplicate User</h1>"    # user better response message

    #return render_template('signup.html', username=username)

@app.route('/single_user')
def home():
    current_user = ''
    user_posts = ''
    if 'user' in session:
        blogs = Blog.query.filter_by(owner_id=session['user']).all()
        return render_template("single_user.html", blogs=blogs)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    title_error = ""
    body_error = ""
    title =""
    body = ""

    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['body']

        if len(title)< 3:
            title_error = "You need a longer title"

        if len(blog)<3:
            body_error = "You need to write a longer post"

        if not title_error and not body_error:
            owner_id = session['user']
            blog = Blog(title, body, owner_id)
            db.session.add(blog)
            db.session.commit()
            return redirect("/individual_blog?id=" + str(blog.id))

        else:
            return render_template('new_post.html', title=title, body=body,
            title_error=title_error, body_error=body_error)

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/blog.html')

@app.route('/individual_blog', methods = ['GET'])
def individual_blog():
    blog_id=request.args.get('id')
    blog = Blog.query.filter_by(id=blog_id).first()
    title = blog.titlebody = blog.body
    author = blog.owner
    return render_template("individual_blog.html", title=title, body=body, author=author)

@app.route('/blog', methods=['POST', 'GET'])
def blogs():
    blog_id = request.args.get('blog.id')
    user_id = request.args.get('user.id')
    if blog_id:
        posts = Blog.query.filter_by(id=blog_id).all()
        return render_template('blog.html', all_blogs=blogs)
    return render_template("blog.html", all_blogs=Blog.query.all())

@app.route('/', methods=[''])
def index():
    users=User.query.all()
    return render_template('index.html', users = users) 


if __name__ == '__main__':
    app.run()