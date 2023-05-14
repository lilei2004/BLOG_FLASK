from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = True


SECRET_KEY = b'a\xe7\xb6\x04\xa4\xb9,\x9eWe\xc7l\ta\x9d\xd1\xc5\xd8\x13\x0f\xb3g0\x8f'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask_student'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
