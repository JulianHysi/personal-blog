"""Module containing the route functions for the posts blueprint.

---

Functions
---------
new_post(): return http response
    the route for creating a new post
post(post_id): return http response
    the route for displaying a post with that id
update_post(post_id): return http response
    the route for updating a post with that id
delete_post(post_id): return http response
    the route for deleting a post with that id
all_posts(): return http response
    the route for displaying all posts
comment(post_id): return http response
    the route for adding a comment to that post
posts_by_tag(tag_content): return http response
    the route for displaying all posts with that tag
tags(): return http response
    the route for displaying all posts, grouped by tag
uploaded_files(filename): return http response, file url
    the route for getting the static file with that filename
upload(): return http response, file url
    the route for uploading a file (post image)
"""

import os
from secrets import token_hex

from flask import Blueprint, render_template, url_for, flash, redirect,\
    request, abort, send_from_directory, current_app
from flask_login import current_user, login_required
from flask_ckeditor import upload_fail, upload_success

from personal_blog import db
from personal_blog.models import Post, Tag, Comment
from personal_blog.posts.forms import PostForm, CommentForm
from personal_blog.posts.utilities import delete_post_images

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """The route for creating a new post.

    If the current user isn't admin, early return code 403.
    If the form validates, create post and tag records.
    Flash the message, and redirect home.
    If it doesn't validate, simply render the template.

    ---

    Returns
    -------
    http response
    """

    if not current_user.is_admin:  # only the admin creates posts
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
        for tag_name in tags:
            tag = Tag(content=tag_name, parent_post=parent_post)
            db.session.add(tag)
        # commit to db
        db.session.commit()
        flash('Post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('posts/create_post.html', title='New Post',
                           form=form, legend='Create Post', hide_sidebar=True)


@posts.route("/post/<int:post_id>")
def post(post_id):
    """The route function for displaying a post with that id.

    Get the post with that id, or return a 404.
    Get the comments for the post, ordered by date posted.
    Get the tags for the post. Render the template.

    ---

    Parameters
    ----------
    post_id: int
        the id of the post to be displayed

    Returns
    -------
    http response
    """

    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(
            Comment.date_posted.asc())
    tags = Tag.query.filter_by(post_id=post_id)
    return render_template('posts/post.html', title=post.title, post=post,
                           comments=comments, tags=tags)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """The route function for updating the post with that id.

    Get the post with that id, or return a 404.
    If the current user isn't the post author, return a 403.
    If the form validates, update the post record, delete the
    old tag records and create new ones, and then commit to db.
    Flash the message, and redirect to that post's route.
    If the form doesn't validate, or the request is GET,
    simply render the template.

    ---

    Parameters
    ----------
    post_id: int
        the id of the post to be updated

    Returns
    -------
    http response
    """

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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        tags = [tag.content for tag in post.tags]
        form.tags.data = ' '.join(tags)
    return render_template('posts/create_post.html', title='Update Post',
                           form=form, legend='Update Post', hide_sidebar=True)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """The route function for deleting the post with that id.

    Get the post with that id, or return a 404.
    If the current user isn't the post author, return a 403.
    Delete the post record, and commit to db.
    Delete the image files associated with that post.
    Flash the message, and redirect home.

    ---

    Parameters
    ----------
    post_id: int
        the id of the post to be deleted

    Returns
    -------
    http response
    """

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # forbidden route
    content = post.content
    db.session.delete(post)
    db.session.commit()
    delete_post_images(content, current_app.root_path)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/all_posts")
def all_posts():
    """The route function for displaying all posts.

    Get current page from the request object.
    Get all posts, ordered by date, and paginated.
    Render the template for the current page.

    ---

    Returns
    -------
    http response
    """

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=current_app.config['PER_PAGE_GLOBAL'])
    return render_template('posts/all_posts.html', posts=posts)


@posts.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def comment(post_id):
    """The route function for adding a comment to that post.

    Get the post with that id, or return a 404.
    If the form validates, create a comment record and commit it.
    Flash the message, and redirect to the post.
    If it doesn't validate, simply render the template.

    ---

    Parameters
    ----------
    post_id: int
        the id of the post to be commented on

    Returns
    -------
    http response
    """

    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id,
                          post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment has been posted!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('posts/comment.html', title='Comment', form=form,
                           post=post, hide_sidebar=True)


@posts.route("/all_posts/<string:tag_content>")
def posts_by_tag(tag_content):
    """The route function for displaying all posts with that tag.

    Collect all the tag records with that tag content.
    Get the corresponding post id for each tag record collected.
    Get the current page from the request object.
    Get all the posts with those post ids, ordered by date
    posted, and paginated.
    Render the template.

    ---

    Parameters
    ----------
    tag_content: str
        the tag whole posts are to be displayed (i.e. 'django')

    Returns
    -------
    http response
    """

    tags = Tag.query.filter_by(content=tag_content).all()
    post_ids = [tag.post_id for tag in tags]
    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Post).filter(Post.id.in_(post_ids)).order_by(
            Post.date_posted.desc()).paginate(
                page=page, per_page=current_app.config['PER_PAGE_GLOBAL'])
    return render_template('posts/posts_by_tag.html', posts=posts,
                           tag=tag_content)


@posts.route("/tags")
def tags():
    """The route function for displaying all posts, grouped by tag.

    Get all distinct tags. Render the template.

    ---

    Returns
    -------
    http response
    """

    tags = db.session.query(Tag.content.distinct().label("content")).all()
    return render_template('posts/tags.html', Tag=Tag, Post=Post, db=db,
                           tags=tags)


@posts.route('/files/<string:filename>')
def uploaded_files(filename):
    """The route function used by Ckeditor for getting uploaded files.

    Get the app path. Pass it on, along with the name
    of the requested file, to send_from_directory().
    Return the output of send_from_directory().

    ---

    Parameters
    ----------
    filename: str
        the name of the file to be retrieved

    Returns
    -------
    http response, filename url
    """

    path = current_app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@posts.route('/upload', methods=['POST'])
def upload():
    """The route function used by Ckeditor for uploading files.

    Get the file from the request object.
    Get its extension. If it's not an image format, return error.
    The reason being, this route is used for post images only.
    Create a random name for the file, and add the extension.
    Save the file with that name in the file system.
    Get the file url using uploaded_files() function above.
    Return the url and a success code.

    ---

    Returns
    -------
    http response, file url
    """

    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    random_hex = token_hex(8)
    filename = ''.join([random_hex, '.', extension])
    f.save(os.path.join(current_app.config['UPLOADED_PATH'], filename))
    url = url_for('posts.uploaded_files', filename=filename)
    return upload_success(url=url)
