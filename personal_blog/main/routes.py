"""Module containing route functions for the main blueprint.

---

Functions
---------
landing_page(): return http response
    the route for the landing page
home(): return http response
    the route for the homepage
about(): return http response
    the route for the about page
search(): return http response
    the route for the search results
"""

from flask import Blueprint, request, render_template, g, redirect, url_for,\
        abort, current_app

from personal_blog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
def landing_page():
    """The route function for the landing page.

    ---

    Returns
    -------
    http response
    """

    return render_template('main/landing_page.html')


@main.route("/home")
def home():
    """The route function for the homepage.

    Display all posts, paginated, from newest to oldest.

    ---

    Returns
    -------
    http response
    """

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=current_app.config['PER_PAGE_HOME'])
    return render_template('main/home.html', posts=posts)


@main.route("/about")
def about():
    """The route function for the about page.

    ---

    Returns
    -------
    http response
    """

    return render_template('main/about.html', title='About')


@main.route("/search")
def search():
    """The route function for the search results page.

    If the search text field is empty, redirect to homepage.
    Get matching posts, paginated, sorted by relevance.
    If the total is -1, elastic isn't running, so return code 500.
    If the total is 0, render the template with the display
    message of no matching results found.
    Else, calculate the next and previous links for the pagination.
    And render the template with the search results.

    ---

    Returns
    -------
    http response
    """

    if not g.search_form.validate():
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE_GLOBAL']
    posts, total = Post.search(g.search_form.q.data, page, per_page)
    if total == -1:
        abort(500)
    elif total == 0:
        return render_template('main/search.html', title='Search',
                               results=False)
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * per_page else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('main/search.html', title='Search', posts=posts,
                           next_url=next_url, prev_url=prev_url, results=True)
