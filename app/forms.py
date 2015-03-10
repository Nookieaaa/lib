from flask import flash
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectMultipleField, widgets
from wtforms.validators import Required, Length
from app.models import User
from database import db_session
from wtforms import validators


class LoginForm(Form):
    email = TextField('email', validators=[validators.required(), validators.Email()])
    password = PasswordField('password', validators=[validators.required()])

    def get_user(self):
        usr = db_session.query(User).filter_by(email=self.email.data).first()
        if not usr:
            usr = db_session.query(User).filter_by(name=self.email.data).first()
        return usr

class BookForm(Form):
    title = TextField('title', validators=[Required(), Length(1, 50)])
    authors = SelectMultipleField('authors', coerce=int, widget=widgets.ListWidget(prefix_label=False),
                                  option_widget=widgets.CheckboxInput())


class AuthorForm(Form):
    name = TextField('name', validators=[Required(), Length(1, 50)])
    books = SelectMultipleField('books', coerce=int, widget=widgets.ListWidget(prefix_label=False),
                                option_widget=widgets.CheckboxInput())


class RegistrationForm(Form):
    name = TextField('name', validators=[validators.required(), Length(6, 50)])
    email = TextField('email', validators=[validators.required(), validators.Email(), Length(max=100)])
    password = PasswordField('password', validators=[validators.required(), Length(max=32)])

    def validate_login(self):
        if db_session.query(User).filter_by(email=self.email.data).count() > 0:
            flash('Email is already registered', 'danger')
            return False
        if db_session.query(User).filter_by(name=self.name.data).count() > 0:
            flash('Name is already in use', 'danger')
            return False
        return True


class SearchForm(Form):
    search = TextField('search', validators=[Length(min=1)])
