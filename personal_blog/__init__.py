from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_mail import Mail
from personal_blog.config import Config

app = Flask(__name__)
app.config.from_object(Config(app.root_path))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)
mail = Mail(app)

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'  # bootstrap class

from personal_blog.main.routes import main 
from personal_blog.users.routes import users
from personal_blog.posts.routes import posts

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)
