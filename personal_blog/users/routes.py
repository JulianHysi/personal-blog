from flask import Blueprint, render_template, url_for, flash, redirect,\
        request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from personal_blog import db, bcrypt
from personal_blog.models import User
from personal_blog.users.forms import RegistrationForm, LoginForm,\
    UpdateAccountForm, RequestResetForm, ResetPasswordForm
from personal_blog.utilities import save_profile_picture, send_reset_email,\
        delete_old_profile_picture, get_sidebar_posts

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
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
    return render_template('register.html', title='Register', form=form,
            hide_sidebar=True)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #'next' is the parameter in the url
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Please enter the right credentials..', 'danger')    
    return render_template('login.html', title='Log In', form=form, hide_sidebar=True)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            delete_old_profile_picture(current_user.profile_pic,\
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

    profile_pic_path = url_for('static',
                filename='profile_pics/' + current_user.profile_pic)

    return render_template('account.html', title='Profile',
            profile_pic_path=profile_pic_path, form=form,
            sidebar_posts=get_sidebar_posts())


@users.route("/account/deactivate", methods=['POST'])
@login_required
def deactivate_account():
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
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password'
                , 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password',
            form=form)


@users.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_token(token):
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
        flash(f'Your password has been updated. '
                'You can proceed with the login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password',
            form=form)
