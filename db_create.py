from app import app, database
import sqlalchemy

db = sqlalchemy(app)
db.create_all()

def main():
  database.init_db()
  database.fill_db()



  