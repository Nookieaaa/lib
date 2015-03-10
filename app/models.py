from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import hashlib


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(100))


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
 #       if self.name == "guest" or self.email=="guest":
 #           return True
        return False

    def get_id(self):
        return unicode(self.id)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        if password:
            self.set_password(password)



    def set_password(self, password):
        hash_object = hashlib.md5(password.encode())

        self.password = hash_object.hexdigest()

    def check_password(self, password):
        hash_object = hashlib.md5(password.encode())
        hash_pw = hash_object.hexdigest()
        return str(hash_pw) == self.password

 

    def __repr__(self):
        return '<User %r>' % self.name


books_authors = Table(
    "books_authors",Base.metadata,
    Column("fk_book", Integer, ForeignKey("books.id")),
    Column("fk_author", Integer, ForeignKey("authors.id")),
    )


class Book(Base):
    __tablename__ = "books"
    __searchable__ = ['title']

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(50), nullable=False)
    authors = relationship(
        "Author",
        backref="books",
        secondary=books_authors
    )

    def __init__(self, title=None):
        self.title = title

    def __repr__(self):
        return '<Book %r>' % self.title


class Author(Base):
    __tablename__ = "authors"
    __searchable__ = ['name']

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50), nullable=False)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Author name: %r>' % self.name
