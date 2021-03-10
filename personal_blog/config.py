"""A module used to store application-wide configuration values

---

Classes
------
    Config: the class used to store general configuration values
    DevelopentConfig: extends Config with development extras
    TestingConfig: extends Config with testing extras
"""

import os


class Config:
    """
    A class used to store configuration values as class constants

    ---

    Class constants
    --------------
    SECRET_KEY : str
        the Flask required, randomly generated secret key
    SQLALCHEMY_DATABASE_URI : str
        the location of the database file used by the application
    SQLALCHEMY_TRACK_MODIFICATIONS : bool
        track modifications of objects and emit signals
    ELASTICSEARCH_URL: str
        url for connecting to the elastic search server

    CKEDITOR_SERVE_LOCAL : bool
        enable serving resources from local when use ckeditor.load(),
        default (False) is to retrieve from CDN
    CKEDITOR_PKG_TYPE : str
        the package type of CKEditor (one of basic, standard or full)
    CKEDITOR_ENABLE_CODESNIPPET : bool
        enable codesnippet plugin of the editor,
        the plugin must be installed (included in built-in resources)
    CKEDITOR_FILE_UPLOADER : str
        the URL or endpoint that handles file upload
    CKEDITOR_HEIGHT : int
        the width of CKEditor textarea, in pixel

    MAIL_SERVER : str
        the server used for sending mails
    MAIL_PORT : int
        the port must match the type of security used
        if using STARTTLS and MAIL_USE_TLS = True, set it to 587
        if using SSL/TLS and MAIL_USE_SSL = True, set it to 465
    MAIL_USE_TLS: bool
        enable TLS security
    MAIL_USERNAME : str
        the username of the account used for sending mails
    MAIL_PASSWORD : str
        the password of the account used for sending mails

    Methods
    -------
    __iter__(self, root_path)
        create instance with UPLOADED_PATH attribute
    """

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_PKG_TYPE = 'standard'
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_FILE_UPLOADER = 'posts.upload'
    CKEDITOR_HEIGHT = 500

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    def __init__(self, root_path):
        """
        Parameters
        ----------
        root_path : str
            the root path of the application
        """

        self.UPLOADED_PATH = os.path.join(root_path, 'static/post_images')


class DevelopmentConfig(Config):
    """
    A class extending base Config, used in development mode

    ---

    Class constants
    ---------------
    DEBUG : bool
        enables interactive debugger and server reload on change
        have it on only when developing, not in production
    """

    DEBUG = True


class TestConfig(Config):
    """
    A class extending base Config, used in testing mode

    ---

    Class constants
    ---------------
    TESTING: bool
        enables exceptions to bubble up even if they're handled by code
        have it on only when testing
    """

    TESTING = True


class ProductionConfig(Config):
    """
    A class extending base Config, used in production

    ---

    Class constants
    ---------------
    TESTING: bool
        enables exceptions to bubble up even if they're handled by code
        have it on only when testing
    """

    TESTING = False
