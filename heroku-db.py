from app import app, database

def main():
  database.init_db()
  database.fill_db()


main()