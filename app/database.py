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
     for insert_line in sql_file.readlines():
       engine.execute(insert_line)
  
if config.HEROKU and "lib.db" not in config.SQLALCHEMY_DATABASE_URI:
  init_db()
  fill_db()

