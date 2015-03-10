import os
APPDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(APPDIR, 'lib.db')

CSRF_ENABLED = True
DEBUG=True
SECRET_KEY = 'SuperSecretKey_S'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(APPDIR, 'lib.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

HEROKU = os.environ.get('HEROKU') is None