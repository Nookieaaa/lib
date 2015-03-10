from app import app, database

def main():
  database.init_db()
  database.fill_db()


if __name__ == "__main__":
  main()