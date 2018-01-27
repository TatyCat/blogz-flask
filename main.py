from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz-flask:password@localhost:8889/blogz-flask'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    blogposts = db.relationship("BlogPost", backref="author")
                                        
    def __init__(self, username, password):
        self.username = username
        self.password = password


class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_published = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author



@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'index', 'allposts']
    if request.endpoint not in allowed_routes and 'username' not in session:
        flash('Please log in to continue')
        return redirect('/login')


@app.route('/', methods=['GET'])
def index():
    # bloggers = User.query.order_by(User.username).all()
    bloggers = User.query.order_by(User.username).all()
    
    return render_template('index.html', bloggers=bloggers)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if username and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect or user does not exist', 'error')
            return redirect('/login')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    author = User.query.filter_by(username=session['username']).first()
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        # author = request.args.get('user.id')
        if title == "" or body == "":
            flash("Please fill out the title and body of your post.", 'error')
            return redirect('/newpost')
        else:
            post = BlogPost(title, body, author)
            db.session.add(post)
            db.session.commit()
            return redirect('/')
    return render_template('newpost.html')


@app.route('/blog/<int:post_id>')
def detailpg(post_id):
    post_id = request.args.get('BlogPost.id')
    post = BlogPost.query.filter_by(id=post_id).one()
    # date_posted = / methods=['GET']
    return render_template('postdetail.html' )


@app.route('/allposts')
def allposts():
    allposts = BlogPost.query.order_by(BlogPost.title).all()
    return render_template('allposts.html', allposts=allposts)


@app.route('/blog/<int:user_id>')
def singleUser(user_id):
    return render_template('singleUser.html')


@app.errorhandler(404) 
def page_not_found(e):
    return render_template('error.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500



if __name__ == '__main__':
    app.run(debug=True)
