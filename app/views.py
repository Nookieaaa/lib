import os
from app import app, lm
from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, login_required, logout_user, current_user
from app.models import User, Book, Author
from database import db_session
from forms import LoginForm, BookForm, AuthorForm, RegistrationForm, SearchForm
import random

#                       User/login
@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

@lm.unauthorized_handler
def unauthorized():
  flash("Login required.", "danger")
  return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/register/', methods=('GET', 'POST'))
def register_view():
  if current_user.is_authenticated():
    flash('sorry, registration is available only for not-authorised users')
    return redirect(url_for('index'))
  form_r = RegistrationForm()
  form=LoginForm()
  if form_r.validate_on_submit() and form_r.validate_login():
      user = User()
      user.name = form_r.name.data
      user.email = form_r.email.data
      user.set_password(form_r.password.data)
      db_session.add(user)
      db_session.commit()
      flash('User %s created succesfully' %(user.email),'success')
      if current_user.is_authenticated():
          logout_user()
      login_user(user)
      return redirect(url_for('index'))
  return render_template('register.html',form = form, form_r=form_r, user=current_user, is_authenticated=current_user.is_authenticated())

@app.route('/login/', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
      user = form.get_user()
      if user and user.check_password(form.password.data):
        login_user(user)
        flash('Welcome ' + user.email, 'success')
        return redirect(request.args.get("next") or url_for("index"))
      else:
        flash('wrong username or password', 'danger')
        return redirect(url_for("login"))
  return render_template("login.html", form=form)


@login_required
@app.route('/logout/')
def logout():
  logout_user()
  flash("You have logged out.", 'info')
  return redirect(url_for('index'))


##                                   index/Search
@app.route('/',methods=('GET', 'POST'))
def index():

    form_s = SearchForm()
    books = db_session.query(Book).all()
    authors = db_session.query(Author).all()


    return render_template("index.html", authors = authors, user=current_user, is_authenticated=current_user.is_authenticated(), books=books, form_s=form_s)


@app.route("/search/", methods=('GET', 'POST'))
def search():

  form_s = SearchForm()
  if form_s.validate_on_submit():
    books = Book.query.all()
    authors = Author.query.all()
    query = form_s.search.data.lower()
    result_books = []
    result_authors = []
    for book in books:
      if query in book.title.lower():
        if not book in result_books:
          result_books.append(book)
    for author in authors:
      if query in author.name.lower():
        result_authors.append(author)
        for b in author.books:
          if not b in result_books:
            result_books.append(b)
    flash("found %s book(s) and %s author(s)" %(len(result_books),len(result_authors)), 'info')
    return render_template('index.html', books=result_books, authors = result_authors, user=current_user,
                         is_authenticated=current_user.is_authenticated(), form_s=form_s)

  return redirect(url_for('index'))


##              BOOKS

@app.route('/books/')
@login_required
def book():
  form = BookForm(request.form)
  books = db_session.query(Book).all()
  return render_template("books.html", user=current_user, books=books,is_authenticated=current_user.is_authenticated())


@app.route('/book_add/', methods=['GET', 'POST'])
@login_required
def book_add():

  book_form = BookForm(request.form)
  book_form.authors.choices = [(p.id, p.name) for p in db_session.query(Author).order_by('id')]

  if book_form.validate_on_submit():
      book = Book()
      book.title = book_form.title.data
      book.authors = [db_session.query(Author).get(o) for o in book_form.authors.data]
      db_session.add(book)
      db_session.commit()
      flash('Successfully added.', 'success')
      return redirect(url_for('index'))

  return render_template("book_create.html", bform=book_form, user=current_user, is_authenticated=current_user.is_authenticated())

@app.route('/book/<id>', methods=['GET', 'POST'])
@login_required
def book_edit(id):

  book = db_session.query(Book).get(id)
  book_form = BookForm(request.form, obj=book)
  book_form.authors.choices = [(p.id, p.name) for p in db_session.query(Author).order_by('id')]

  if book_form.validate_on_submit():
      book = db_session.query(Book).get(id)
      book.title = book_form.title.data
      book.authors = [db_session.query(Author).get(o) for o in book_form.authors.data]
      db_session.commit()
      flash('Changes saved', 'info')
      return redirect(url_for('index'))

  book_form.authors.data = [p.id for p in book.authors]
  return render_template("book.html", bform=book_form, book=book, user=current_user, is_authenticated=current_user.is_authenticated())


@app.route('/book_rm/<id>', methods=['GET', 'POST'])
@login_required
def book_rm(id):
  book = db_session.query(Book).get(id)
  if book:
      db_session.delete(book)
      db_session.commit()
      flash('Deleted successfully.', 'warning')
  return redirect(url_for('index'))




##            AUTHORS
@app.route('/authors/')
@login_required
def author():

  authors = db_session.query(Author).all()
  return render_template("authors.html", user=current_user, is_authenticated=current_user.is_authenticated(), authors=authors)


@app.route('/author/<id>', methods=['GET', 'POST'])
@login_required
def author_edit(id):

  author = db_session.query(Author).get(id)
  author_form = AuthorForm(request.form, obj=author)
  author_form.books.choices = [(b.id, b.title) for b in db_session.query(Book).order_by('id')]

  if author_form.validate_on_submit():
      author = db_session.query(Author).get(id)
      author.name = author_form.name.data
      author.books = [db_session.query(Book).get(b) for b in author_form.books.data]
      db_session.commit()
      flash('Changes saved', 'info')
      return redirect(url_for('index'))

  author_form.books.data = [auth.id for auth in author.books]
  return render_template("author.html", bform=author_form, author=author, user=current_user, is_authenticated=current_user.is_authenticated())


@app.route('/author_add/', methods=['GET', 'POST'])
@login_required
def author_add():
  author_form = AuthorForm(request.form)
  author_form.books.choices = [(p.id, p.title) for p in db_session.query(Book).order_by('id')]

  if author_form.validate_on_submit():
      author = Author()
      author.name = author_form.name.data
      author.books = [db_session.query(Book).get(o) for o in author_form.books.data]
      db_session.add(author)
      db_session.commit()
      flash('Successfully added.', 'success')
      return redirect(url_for('index'))

  return render_template("author_create.html", bform=author_form, user=current_user, is_authenticated=current_user.is_authenticated())


@app.route('/author_rm/<id>', methods=['GET', 'POST'])
@login_required
def author_rm(id):
  author = db_session.query(Author).get(id)
  if author:
      db_session.delete(author)
      db_session.commit()
      flash('Deleted.', 'warning')
  return redirect(url_for('index'))

# random page
@app.route('/random', methods=['GET', 'POST'])
def random_page():
  boa=random.randint(1,2)   #boa = book(1) or author(2)
  id_list=[]
  if boa == 1:
    authors = db_session.query(Author).all()
    for i in authors: id_list.append(i.id)
    randid= random.choice(id_list)
    return redirect('/author/'+str(randid))
  books = db_session.query(Book).all()
  for i in books: id_list.append(i.id)
  randid= random.choice(id_list)
  return redirect('/book/'+str(randid))


