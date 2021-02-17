from flask import Blueprint, render_template, url_for, flash, redirect, abort,\
        request
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


@books.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book,
                           sidebar_posts=get_sidebar_posts())


@books.route("/book/<int:book_id>/update", methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not current_user.is_admin:  # only the admin can update books
        abort(403)  # forbidden route
    form = BookForm()
    form.submit.label.text = 'Update'
    if form.validate_on_submit():
        book.title = form.title.data
        book.authors = form.authors.data
        book.edition = form.edition.data
        if form.link.data:
            book.link = form.link.data
        book.description = form.description.data
        db.session.commit()
        flash('Book has been updated!', 'success')
        return redirect(url_for('books.book', book_id=book.id))
    elif request.method == 'GET':
        form.title.data = book.title
        form.authors.data = book.authors
        form.edition.data = book.edition
        form.link.data = book.link
        form.description.data = book.description
    return render_template('add_book.html', title='Update Book',
                           form=form, legend='Update Book', hide_sidebar=True)
