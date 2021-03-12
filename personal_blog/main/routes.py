from flask import Blueprint, request, render_template, g, redirect, url_for,\
        abort, current_app

from personal_blog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
def landing_page():
    return render_template('main/landing_page.html')


@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=current_app.config['PER_PAGE_HOME'])
    return render_template('main/home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')


@main.route("/search")
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, 3)
    if total == -1:
        abort(500)
    elif total == 0:
        return render_template('main/search.html', title='Search',
                               results=False)
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * 6 else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('main/search.html', title='Search', posts=posts,
                           next_url=next_url, prev_url=prev_url, results=True)
