from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt #a password hashing utility
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY') #environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')  #environment variable
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' #bootstrap class

from personal_blog import routes
