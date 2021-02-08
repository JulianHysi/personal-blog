from personal_blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', cascade='all, delete',
            lazy=True)
    #'Post' in uppercase because it references the class name
    comments = db.relationship('Comment', backref='author', cascade='all,delete',
            lazy=True)

    def __repr__(self):
        return f"User: {self.username}, \nEmail: {self.email}\n"

    def get_reset_token(self, expiration_secs=600):
        serializer = Serializer(current_app.config['SECRET_KEY'],
                expiration_secs)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #'user' in lowercase because it references the table name
    comments = db.relationship('Comment', cascade='all,delete', backref='parent_post', lazy=True)
    tags = db.relationship('Tag', cascade='all,delete', backref='parent_post', lazy=True)
    pics = db.relationship('Picture', cascade='all,delete', backref='parent_post', lazy=True)
    
    def __repr__(self):
        return f"Blog post: {self.title}, \nPosted on: {self.date_posted}\n"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(20), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class Picture(db.Model):
    pic = db.Column(db.String(20), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
