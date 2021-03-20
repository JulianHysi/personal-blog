"""Module containing utility/helper functions for the main blueprint.

---

Functions
---------
sidebar_posts(): dict
    the function that gets the posts to be displayed on the sidebar
before_request(): None
    the function executed before each request
"""

from flask import current_app, g


from personal_blog.models import Post
from personal_blog.main.forms import SearchForm
from personal_blog.main.routes import main


@current_app.context_processor
def sidebar_posts():
    """The function that gets the posts to be displayed on the sidebar.

    Get the 5 latest posts. Return a dict with 1 element.
    The key is sidebar_posts, the value is the posts collected earlier.

    ---

    Returns
    -------
    dict with a sidebar_posts key and the posts list as a value
    """

    posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    return dict(sidebar_posts=posts)


@main.before_app_request
def before_request():
    """The function executed before each request.

    Create an instance of SearchForm. Store it in the g global.
    It needs to be avilable everywhere, because the search bar is.
    A user can launch a search from any part of the application.
    """

    g.search_form = SearchForm()
