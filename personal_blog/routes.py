import os
from secrets import token_hex
from flask import render_template, url_for, flash, redirect, request, abort,\
        send_from_directory
from personal_blog import app, db, bcrypt, ckeditor
from personal_blog.models import User, Post, Comment, Tag
from personal_blog.forms import RegistrationForm, LoginForm, PostForm,\
        UpdateAccountForm, CommentForm, RequestResetForm, ResetPasswordForm
from personal_blog.utilities import delete_old_profile_picture
from personal_blog.utilities import save_profile_picture, delete_post_images
from personal_blog.utilities import send_reset_email
from flask_login import login_user, logout_user, current_user, login_required
from flask_ckeditor import upload_fail, upload_success

sidebar_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int) #url query parameter
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('home.html', posts=posts, sidebar_posts=sidebar_posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About', sidebar_posts=sidebar_posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form,
            hide_sidebar=True)


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
    return render_template('login.html', title='Log In', form=form, hide_sidebar=True)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            delete_old_profile_picture(current_user.profile_pic, app.root_path)
            profile_pic_file = save_profile_picture(form.profile_pic.data,
                    app.root_path)
            current_user.profile_pic = profile_pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_pic_path = url_for('static',
                filename='profile_pics/' + current_user.profile_pic)

    return render_template('account.html', title='Profile',
            profile_pic_path=profile_pic_path, form=form,
            sidebar_posts=sidebar_posts)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.is_admin != True:  # only the admin creates posts
        abort(403)  
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                author=current_user)
        db.session.add(post)
        # add tags
        tags = form.tags.data
        tags = tags.split(' ')
        parent_post = Post.query.order_by(Post.date_posted.desc()).first()
        for i in tags:
            tag = Tag(content=i, parent_post=parent_post)
            db.session.add(tag)
        # commit to db
        db.session.commit()
        flash('Post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', 
                            form=form, legend='Create Post', hide_sidebar=True)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(
            Comment.date_posted.asc())
    tags = Tag.query.filter_by(post_id=post_id)
    has_comments = len(list(comments)) > 0
    return render_template('post.html', title=post.title, post=post,
            comments=comments, sidebar_posts=sidebar_posts,
            has_comments=has_comments, tags=tags)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # forbidden route
    form = PostForm()
    form.submit.label.text = 'Update'
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        old_tags = Tag.query.filter_by(post_id=post_id)
        for tag in old_tags:
            db.session.delete(tag)
        new_tags = form.tags.data
        new_tags = new_tags.split(' ')
        for i in new_tags:
            tag = Tag(content=i, parent_post=post)
            db.session.add(tag)  
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        tags = [tag.content for tag in post.tags]
        form.tags.data = ' '.join(tags)
    return render_template('create_post.html', title='Update Post',
                            form=form, legend='Update Post', hide_sidebar=True)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # forbidden route
    content = post.content
    db.session.delete(post)    
    db.session.commit()
    delete_post_images(content, app.root_path)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/all_posts")
def all_posts():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('all_posts.html', posts=posts,
            sidebar_posts=sidebar_posts)


@app.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id,
                post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment has been posted!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return render_template('comment.html', title='Comment', form=form,
            post=post, hide_sidebar=True)


#returns all posts for a certain tag
@app.route("/all_posts/<string:tag_content>")
def posts_by_tag(tag_content):
    tags = Tag.query.filter_by(content=tag_content).all()
    post_id_set = set()
    for tag in tags:
        post_id_set.add(tag.post_id)
    posts = db.session.query(Post).filter(Post.id.in_(post_id_set)).order_by(
            Post.date_posted.desc()).all()
    return render_template('all_posts.html', posts=posts,
            sidebar_posts=sidebar_posts, tag=tag_content)


#returns all tags, and the number of posts they have
@app.route("/tags")
def tags():
    tags = db.session.query(Tag.content.distinct().label("content")).all()
    return render_template('tags.html', Tag=Tag, Post=Post, db=db, tags=tags)


@app.route("/account/deactivate", methods=['POST'])
@login_required
def deactivate_account():
    if current_user.is_admin:
        flash('Admin account cannot be deactivated', 'danger')
        return redirect(url_for('account'))
    filename = current_user.profile_pic
    db.session.delete(current_user)    
    db.session.commit()
    delete_old_profile_picture(filename, root_path=app.root_path)
    flash('Your account has been deactivated!', 'success')
    return redirect(url_for('logout'))


@app.route('/files/<string:filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    random_hex = token_hex(8)
    filename = ''.join([random_hex, '.', extension])
    f.save(os.path.join(app.config['UPLOADED_PATH'], filename))
    url = url_for('uploaded_files', filename=filename)
    return upload_success(url=url)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password'
                , 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password',
            form=form)


@app.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid/expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        passwd = form.password.data
        hashed_passwd = bcrypt.generate_password_hash(passwd).decode('utf-8')
        user.password = hashed_passwd
        db.session.commit()
        flash(f'Your password has been updated. '
                'You can proceed with the login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password',
            form=form)
