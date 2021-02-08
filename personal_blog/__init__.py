from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_mail import Mail
from personal_blog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
ckeditor = CKEditor()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'  # bootstrap class


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config(app.root_path))

    db.init_app(app)
    bcrypt.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from personal_blog.main.routes import main 
    from personal_blog.users.routes import users
    from personal_blog.posts.routes import posts
    from personal_blog.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
