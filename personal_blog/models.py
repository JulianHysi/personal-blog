from personal_blog import db, login_manager # __main__ == flaskblog.py in this case. Avoids circular importing.
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#ignore errors on db object..it's an internal VS Code/pylint issue
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #'Post' in uppercase because it references the class name

    def __repr__(self):
        return f"User: {self.username}, \nEmail: {self.email}\n"


#ignore errors on db object..it's an internal VS Code/pylint issue
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #'user' in lowercase because it references the table name

    def __repr__(self):
        return f"Blog post: {self.title}, \nPosted on: {self.date_posted}\n"   
