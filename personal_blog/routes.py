from flask import render_template, url_for, flash, redirect
from personal_blog import app
from personal_blog.models import User, Post #import statement moved down here, to avoid circular importing issue
from personal_blog.forms import RegistrationForm, LoginForm

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