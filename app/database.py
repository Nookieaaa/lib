from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=config.DEBUG,convert_unicode=True)


db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()



def init_db():
    import models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)



def fill_db():
  with open('fill_data.sql', 'r') as sql_file:
    from models import Book,Author
    book1 = Book()
    book1.title = 'Head First Design Patterns'
    db_session.add(book1)
    book2 = Book()
    book2.title = 'C++ Primer Plus (6th Edition)'
    db_session.add(book2)
    book3 = Book()
    book3.title = 'Waite Group''s Microsoft Quickbasic Primer Plus'
    db_session.add(book3)
    book4 = Book()
    book4.title = 'Head First Java'
    db_session.add(book4)
    book5 = Book()
    book5.title = 'Elixir Cookbook'
    db_session.add(book5)
    book6 = Book()
    book6.title = 'Clojure Web Development Essentials'
    db_session.add(book6)
    db_session.commit()

    author1 = Author()
    author1.name ='Elisabeth Freeman'
    db_session.add(author1)
    author2 = Author()
    author2.name ='Eric Freeman'
    db_session.add(author2)
    author3 = Author()
    author3.name ='Bert Bates'
    db_session.add(author3)
    author4 = Author()
    author4.name ='Kathy Sierra'
    db_session.add(author4)
    author5 = Author()
    author5.name ='Elisabeth Robson'
    db_session.add(author5)
    author6 = Author()
    author6.name ='Stephen Prata'
    db_session.add(author6)
    db_session.commit()


    for insert_line in sql_file.readlines():
      engine.execute(insert_line)
  


