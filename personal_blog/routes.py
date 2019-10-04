import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from personal_blog import app, db, bcrypt
from personal_blog.models import User, Post, Comment, Tag
from personal_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm
from flask_login import login_user, logout_user, current_user, login_required


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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account {form.username.data} has been registered. You can proceed with the login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, hide_sidebar=True)

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

def save_profile_picture(profile_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(profile_pic.filename)
    filename = random_hex + f_ext #the name with which the file picture will be saved
    filepath = os.path.join(app.root_path, 'static/profile_pics', filename)

    file_dimensions = (125, 125) #force these dimensions into the save filed
    image = Image.open(profile_pic)
    image.thumbnail(file_dimensions)

    image.save(filepath)
    return filename

def delete_old_profile_picture():
    filename = current_user.profile_pic
    filepath = os.path.join(app.root_path, 'static/profile_pics', filename)
    try:
        os.remove(filepath)
    except:
        pass

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            delete_old_profile_picture() # deletes the old profile picture file from the filesystem
            profile_pic_file = save_profile_picture(form.profile_pic.data)
            current_user.profile_pic = profile_pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email   
    profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('account.html', title='Profile', profile_pic=profile_pic, form=form, sidebar_posts=sidebar_posts)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.is_admin != True:   #only the admin should create posts
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        tags = form.tags.data
        tags = tags.split(' ')
        parent_post = Post.query.order_by(Post.date_posted.desc()).first()
        for i in tags:
            tag = Tag(content=i, parent_post=parent_post)
            db.session.add(tag)
        db.session.commit()
        flash('Post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', 
                            form=form, legend='Create Post', hide_sidebar=True)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date_posted.desc())
    tags = Tag.query.filter_by(post_id=post_id)
    has_comments = len(list(comments)) > 0
    return render_template('post.html', title=post.title, post=post, comments=comments, 
                           sidebar_posts=sidebar_posts, has_comments=has_comments, tags=tags)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #forbidden route
    form = PostForm()
    form.submit.label.text = 'Update' # submit button has a label of 'Update' in this case
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
        tags = list()
        for tag in post.tags:
            tags.append(tag.content)
        tag_str = ' '.join(tags)    
        form.tags.data = tag_str
    return render_template('create_post.html', title='Update Post',
                            form=form, legend='Update Post', hide_sidebar=True)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #forbidden route
    db.session.delete(post)    
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/all_posts")
def all_posts():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('all_posts.html', posts=posts, sidebar_posts=sidebar_posts)

@app.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment has been posted!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return render_template('comment.html', title='Comment', form=form, post=post, hide_sidebar=True)

#returns all posts for a certain tag
@app.route("/all_posts/<string:tag_content>")
def posts_by_tag(tag_content):
    tags = Tag.query.filter_by(content=tag_content).all()
    post_id_set = set()
    for tag in tags:
        post_id_set.add(tag.post_id)
    posts = db.session.query(Post).filter(Post.id.in_(post_id_set)).order_by(Post.date_posted.desc()).all()
    return render_template('all_posts.html', posts=posts, sidebar_posts=sidebar_posts, tag=tag_content)

#returns all tags, and the number of posts they have
@app.route("/tags")
def tags():
    tags = db.session.query(Tag.content.distinct().label("content")).all()
    return render_template('tags.html', Tag=Tag, Post=Post, db=db, tags=tags)