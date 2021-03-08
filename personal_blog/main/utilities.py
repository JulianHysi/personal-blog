from flask import current_app, g


from personal_blog.models import Post
from personal_blog.main.forms import SearchForm
from personal_blog.main.routes import main


@current_app.context_processor
def sidebar_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    return dict(sidebar_posts=posts)


@main.before_app_request
def before_request():
    g.search_form = SearchForm()
