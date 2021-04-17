"""A module mainly used to store SQLAlchemy database models.

---

Functions
---------
load_user(user_id): return an instance of class User
    used by login_manager extension for loading users


Classes
-------
SearchableMixin: SearchableMixin
    mixin class which provides full-text search functionality
User: inherits from SQLAlchemy.Model and flask_login.UserMixin
    db class used for modelling user records
Post: inherits from SQLAlchemy.Model and SearchableMixin
    db class used for modelling post records
Comment: inherits from SQLAlchemy.Model
    db class used for modelling post comment records
Tag: inherits from SQLAlchemy.Model
    db class used for modelling post tag records
Book: inherits from SQLAlchemy.Model
    db class used for modelling book records
"""

from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin

from personal_blog import db, login_manager
from personal_blog.search import add_to_index, remove_from_index, query_index


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class SearchableMixin():
    """A glue layer between the SQLAlchemy and Elasticsearch worlds.

    ---

    Class Methods
    -------------
    search(cls, expression, page, per_page): return result set, total
        search for the given expression and paginate results
    before_commit(cls, session): return None
        store session changes before they are commited (and lost)
    after_commit: return None
        add the stored session changes to the index database
    reindex(cls): return None
        reindex (to the index database) the caller table
    """

    @classmethod
    def search(cls, expression, page, per_page):
        """Search for the given expression and paginate results.

        Get the matching posts' ids and their total.
        Depending on total's value, different actions are taken.
        If the total is -1, elastic server isn't set up or running.
        That's still okay, because the search feature is optional.
        If the total is 0, no matching result was found.
        Else, use the post ids to get the records from the table.

        ---

        Parameters
        ----------
        expression: str
            the text to search for
        page: int
            the current page number of the (paginated) result set
        per_page: int
            the number by which pages are being paginated

        Returns
        -------
        the result set: SQLAlechemy.BaseQuery class instance
            it's empty when the total is -1 or zero
        the total: int
            can be -1, 0 or a natural number, see description above
        """

        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == -1:
            return cls.query.filter_by(id=0), -1
        elif total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        """Store session changes before they are commited.

        Used to keep in sync the main database with the index one.
        The changes made to main database are part of the session.
        These changes should be reflected on the index database too.
        But once the session is commited to main, the changes are lost.
        Therefore, store them in a dict before the commit.
        And use the dict to apply them after commit, to the index db.
        """

        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        """Add the saved session changed to the index database.

        Used to keep in sync the main database with the index one.
        The changes made to the main database were stored in a dict.
        These changes should be reflected on the index database too.
        Read the dict and apply the changes. Then, empty the dict.
        """

        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """Reindex to the index database the caller table class."""
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class User(db.Model, UserMixin):
    """ORM class used for modelling users and their behavior.

    Inherit for SQLAlchemy.Model and login_manager.UserMixin.
    Create class variables which the ORM uses as table columns.

    ---

    Class variables
    ---------------
    id : SQLALchemy.Column
        integer, primary key
    username: SQLALchemy.Column
        string, unique, mandatory, indexed
    profile_pic: SQLALchemy.Column
        filepath string, mandatory, defaults to default.png
    password: SQLALchemy.Column
        hashed string, mandatory
    is_admin: SQLALchemy.Column
        boolean, defaults to False, only 1 user can have it set to True
    posts: SQLAlchemy.relationship
        every post record has a user author, delete on cascade
    comments: SQLAlchemy.relationship
        every comment record has a user author, delete on cascade

    Methods
    -------
    __repr__(self): str
        string representation of a User instance
    get_reset_token(self, expiration_secs): str
        get a password reset token for the user
    verify_reset_token(token): User instance or None
        get back the user if with that password reset token
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True,
                         nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False,
                            default='default.png')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', cascade='all, delete',
                            lazy=True)
    # 'Post' in uppercase because it references the class name
    comments = db.relationship('Comment', backref='author',
                               cascade='all,delete', lazy=True)

    def __repr__(self):
        return f"User: {self.username}, \nEmail: {self.email}\n"

    def get_reset_token(self, expiration_secs=600):
        """Get a password reset token.

        ---

        Parameters
        ----------
        expiration_secs: int
            seconds after which the token expires, defaults to 600

        Returns
        -------
        the reset token: str
            the token received from the serializer and decoded to str
        """

        serializer = Serializer(current_app.config['SECRET_KEY'],
                                expiration_secs)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """Static method, verify password reset token.

        ---

        Parameters
        ----------
        token: str
            the password reset token to be verified

        Returns
        -------
        the verified user: User instance
            the user queried by the user_id on the token load
        """

        serializer = Serializer(current_app.config['SECRET_KEY'])
        user_id = serializer.loads(token)['user_id']
        return User.query.get(user_id)


class Post(SearchableMixin, db.Model):
    """ORM class used for modelling posts and their behavior.

    Inherit for SQLAlchemy.Model and SearchableMixin.
    Create class variables which the ORM uses as table columns.

    ---

    Class variables
    ---------------
    __searchable__ : list[str]
        names of columns which should be full-text searched
    id : SQLALchemy.Column
        integer, primary key
    title: SQLALchemy.Column
        string, mandatory, indexed
    date_posted: SQLALchemy.Column
        datetime, mandatory, indexed, defaults to utcnow
    content: SQLALchemy.Column
        text, mandatory
    user_id: SQLALchemy.Column
        integer, foreign key, points to User.id
    tags: SQLAlchemy.relationship
        every tag record has a parent post, delete on cascade
    comments: SQLAlchemy.relationship
        every comment record has a parent post, delete on cascade

    Methods
    -------
    __repr__(self): str
        string representation of a Post instance
    """

    __searchable__ = ['content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, index=True,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 'user' above is in lowercase because it references the table name
    comments = db.relationship('Comment', cascade='all,delete',
                               backref='parent_post', lazy=True)
    tags = db.relationship('Tag', cascade='all,delete', backref='parent_post',
                           lazy=True)

    def __repr__(self):
        return f"Blog post: {self.title}, \nPosted on: {self.date_posted}\n"


class Comment(db.Model):
    """ORM class used for modelling comments.

    Inherit for SQLAlchemy.Model.
    Create class variables which the ORM uses as table columns.

    ---

    Class variables
    ---------------
    id : SQLALchemy.Column
        integer, primary key
    date_posted: SQLALchemy.Column
        datetime, mandatory, indexed, defaults to utcnow
    content: SQLALchemy.Column
        text, mandatory
    user_id: SQLALchemy.Column
        integer, foreign key, points to User.id
    post_id: SQLALchemy.Column
        integer, foreign key, points to Post.id

    Methods
    -------
    __repr__(self): str
        string representation of a Comment
    """

    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, index=True,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Comment {self.id} by user {self.user_id} for "\
                f"post {self.post_id}\n"


class Tag(db.Model):
    """ORM class used for modelling tags.

    Inherit for SQLAlchemy.Model.
    Create class variables which the ORM uses as table columns.

    ---

    Class variables
    ---------------
    id : SQLALchemy.Column
        integer, primary key
    content: SQLALchemy.Column
        string, mandatory
    post_id: SQLALchemy.Column
        integer, foreign key, points to Post.id

    Methods
    -------
    __repr__(self): str
        string representation of a Tag
    """

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(20), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Tag {self.id} for post {self.post_id}\n"


class Book(db.Model):
    """ORM class used for modelling books.

    Inherit for SQLAlchemy.Model.
    Create class variables which the ORM uses as table columns.

    ---

    Class variables
    ---------------
    id : SQLALchemy.Column
        integer, primary key
    title: SQLALchemy.Column
        string, mandatory, indexed
    authors: SQLALchemy.Column
        string, mandatory
    edition: SQLAlchemy.Column
        string, mandatory
    link: SQLAlchemy.Column
        string
    description: SQLAlchemy.Column
        text, mandatory

    Methods
    -------
    __repr__(self): str
        string representation of a Book
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, index=True)
    authors = db.Column(db.String(60), nullable=False)
    edition = db.Column(db.String(20), nullable=False)
    link = db.Column(db.String(60))
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Book {self.id} titled {self.title}\n"
