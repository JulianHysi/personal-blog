from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '0ab581061e7206cf1055587676133539' #make it an env variable later on
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

#ignore errors on db object..it's an internal VS Code/pylint issue
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #'Post' in uppercase because it references the class name

    def __repr__(self):
        return f"User: {self.username}, \nEmail: {self.email}\n"


#ignore errors on db object..it's an internal VS Code/pylint issue
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #'user' in lowercase because it references the table name

    def __repr__(self):
        return f"Blog post: {self.title}, \nPosted on: {self.date_posted}\n"   


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account registered for user: {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'julian@live.com':
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please enter the right credentials..', 'danger')    
    return render_template('login.html', title='Log In', form=form)

if __name__ == '__main__':
    app.run(debug=True)