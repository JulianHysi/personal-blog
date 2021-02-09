from personal_blog.models import Post


def get_sidebar_posts():
    return Post.query.order_by(Post.date_posted.desc()).limit(5).all()
