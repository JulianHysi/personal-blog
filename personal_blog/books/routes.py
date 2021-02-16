from flask import Blueprint, render_template, url_for, flash, redirect, abort
from flask_login import current_user, login_required

from personal_blog import db
from personal_blog.models import Book
from personal_blog.books.forms import BookForm
from personal_blog.main.utilities import get_sidebar_posts

books = Blueprint('books', __name__)


@books.route("/book/new", methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin:  # only the admin adds books
        abort(403)
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, authors=form.authors.data,
                    link=form.link.data, edition=form.edition.data,
                    description=form.description.data)
        db.session.add(book)
        db.session.commit()
        flash('Book has been added!', 'success')
        return redirect(url_for('books.all_books'))
    return render_template('add_book.html', title='New Book',
                           form=form, legend='Add Book', hide_sidebar=True)


@books.route("/all_books")
def all_books():
    books = Book.query.all()
    return render_template('all_books.html', books=books,
                           sidebar_posts=get_sidebar_posts())
