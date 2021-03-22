"""Module containing the route functions for the users blueprint.

---

Functions
---------
register(): return http response
    the route for registering a new user
login(): return http response
    the route for logging a user in
logout(): return http response
    the route for loggin a user out
account(): return http response
    the route for displaying a user account
deactivate_account(): return http response
    the route for deactivating a user account
reset_request(): return http response
   the route for requesting a password reset
reset_token(): return http response
    the route for resetting the password
"""

from flask import Blueprint, render_template, url_for, flash, redirect,\
        request, current_app
from flask_login import login_user, current_user, logout_user, login_required

from personal_blog import db, bcrypt
from personal_blog.models import User
from personal_blog.users.forms import RegistrationForm, LoginForm,\
    UpdateAccountForm, RequestResetForm, ResetPasswordForm
from personal_blog.users.utilities import save_profile_picture,\
        delete_old_profile_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """The route for registering a new user.

    If the current user is already authenticated, redirect home.
    If the form validates, create the new user and commit to db.
    Hash the passsword first. Set the is_admin property to yes
    if no other user has it on (there can be only 1 admin).
    Flash the message, and redirect to the login route.
    If the form doesn't validate, simply render the template.

    ---

    Returns
    -------
    http response
    """

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        passwd = form.password.data
        hashed_passwd = bcrypt.generate_password_hash(passwd).decode('utf-8')
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password = hashed_passwd
        user.is_admin = 0 if User.query.filter_by(is_admin=1).first() else 1
        db.session.add(user)
        db.session.commit()
        flash(f'Account {form.username.data} has been registered. '
              'You can proceed with the login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form,
                           hide_sidebar=True)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """The route for logging a user in.

    If the user is already authenticated, redirect home.
    If the form validates, and the credentials match a
    user in the db, log the user in.
    Get the next page url parameter from the request object.
    If there is a next page, redirect to it. Else, to home.
    If the form validates, but credentials dont match,
    flash a warning message.
    If he form doesn't validate, simply render the template.

    ---

    Returns
    -------
    http response
    """

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # url parameter
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Please enter the right credentials..', 'danger')
    return render_template('users/login.html', title='Log In', form=form,
                           hide_sidebar=True)


@users.route("/logout")
def logout():
    """The route for logging a user out.

    Log the user out, and redirect home.

    ---

    Returns
    -------
    http response
    """

    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """The route for displaying/editing a user account profile.

    If the form validates, update the current user.
    If there was an update of profile picture, delete the old
    one from the filesystem, and store the new one.
    Commit to db, flash the message, and redirect to this route.
    If the form doesn't validate and request is GET, simply
    preload the account form with data, and render the template.

    ---

    Returns
    -------
    http response
    """

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            delete_old_profile_picture(current_user.profile_pic,
                                       current_app.root_path)
            profile_pic_file = save_profile_picture(form.profile_pic.data,
                                                    current_app.root_path)
            current_user.profile_pic = profile_pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_pic_path = url_for(
        'static', filename='profile_pics/' + current_user.profile_pic)

    return render_template('users/account.html', title='Profile',
                           profile_pic_path=profile_pic_path, form=form)


@users.route("/account/deactivate", methods=['POST'])
@login_required
def deactivate_account():
    """The route for deactivating a user account.

    If the current user is admin, do not allow the deactivation.
    Flash the message, and redirect to that user's account.
    Else, delete the current user, commit to db, delete their
    profile picture from the filesystem, flash the message, and
    redirect to the logout route.

    ---

    Returns
    -------
    http response
    """

    if current_user.is_admin:
        flash('Admin account cannot be deactivated', 'danger')
        return redirect(url_for('users.account'))
    filename = current_user.profile_pic
    db.session.delete(current_user)
    db.session.commit()
    delete_old_profile_picture(filename, root_path=current_app.root_path)
    flash('Your account has been deactivated!', 'success')
    return redirect(url_for('users.logout'))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """The route for requesting a password reset.

    If the current user is authenticated, redirect home.
    If the form validates, get the user with that email.
    If the user exists, send the reset email. But flash
    the message anyway as a security best practice, and
    redirect to the login route.
    If the form doesn't validate, simply render the template.

    ---

    Returns
    -------
    http response
    """

    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('An email has been sent with instructions to reset '
              'your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password',
                           form=form)


@users.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_token(token):
    """The route for resetting the password.

    If the current user is authenticated, redirect home.
    If the token isn't valid, flash the message and
    redirect to the reset_request route.
    If the form validates, get the new password, hash its
    value and update the user with it.
    Commit to db, flash the message and redirect to login.
    If the form doesn't validate, simply render the template.

    ---

    Returns
    -------
    http response
    """

    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid/expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        passwd = form.password.data
        hashed_passwd = bcrypt.generate_password_hash(passwd).decode('utf-8')
        user.password = hashed_passwd
        db.session.commit()
        flash('Your password has been updated. '
              'You can proceed with the login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password',
                           form=form)
