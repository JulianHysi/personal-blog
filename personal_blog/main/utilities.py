from flask import current_app

from personal_blog.models import Post


@current_app.context_processor
def sidebar_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    return dict(sidebar_posts=posts)
