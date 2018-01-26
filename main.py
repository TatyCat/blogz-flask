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
    password = db.Column(db.String(25), nullable=False)
    blogpost = db.relationship("BlogPost", back_populates="user")
                                            # backref = 'user')
    def __init__(self, username):
        self.username = username


class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_published = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship("User", back_populates="blogpost")
    # blog_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, text, title, date_published):
        self.text = text
        self.title = title
        self.date_published = published

@app.route('/', methods=['GET'])
def index():
    bloggers = BlogPost.query.all()
    return render_template('index.html', bloggers=bloggers)

# @app.before_request
# def require_login():
#     allowed_routes = ['login', 'register']
#     if request.endpoint not in allowed_routes and 'email' not in session:
#         return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if username and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/newpost')
def new_post():
    title = request.form['title']
    text = request.form['text']
    author = request.form['author']
    post = BlogPost(title=title, text=text, author=author, date_posted=date_posted.now())
    return (url_for('index'))


@app.route('/blog/<int:post_id>')
def detailpg(post_id):
    post = BlogPost.query.filter_by(id=post_id).one()
    # date_posted = / methods=['GET']
    return render_template('postdetail.html', )


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
