from flask import Blueprint, request, render_template

from personal_blog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
def landing_page():
    return render_template('main/landing_page.html')


@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)  # url query parameter
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=6)
    return render_template('main/home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')
