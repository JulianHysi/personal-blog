from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '0ab581061e7206cf1055587676133539' #make it an env variable later on

posts = [
    {
        'author': 'Julian Hysi',
        'title': 'First blog post',
        'content': 'First blog post contents',
        'date_posted': 'August 2019, 15 (?)'
    },
    {
        'author': 'Albor Hysi',
        'title': 'Second blog post',
        'content': 'Second blog post contents',
        'date_posted': 'August 2019, 15 (defo)'
    }

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