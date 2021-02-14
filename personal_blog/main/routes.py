from flask import Blueprint, request, render_template

from personal_blog.models import Post
from personal_blog.main.utilities import get_sidebar_posts

main = Blueprint('main', __name__)


@main.route("/")
def landing_page():
    return render_template('landing_page.html')


@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)  # url query parameter
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=6)
    return render_template('home.html', posts=posts,
                           sidebar_posts=get_sidebar_posts())


@main.route("/about")
def about():
    return render_template('about.html', title='About',
                           sidebar_posts=get_sidebar_posts())
