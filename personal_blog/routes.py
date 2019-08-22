from flask import render_template, url_for, flash, redirect, request
from personal_blog import app, db, bcrypt
from personal_blog.models import User, Post #import statement moved down here, to avoid circular importing issue
from personal_blog.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        'author': 'Julian Hysi',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 20, 2019'
    },
    {
        'author': 'Al Pacino',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 23, 2019'
    } # dummy data just for testing purposes, will be deleted later
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account {form.username.data} has been registered. You can proceed with the login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #'next' is the parameter in the url
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Please enter the right credentials..', 'danger')    
    return render_template('login.html', title='Log In', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Profile')