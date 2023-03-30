SECRET_KEY = "test"
TOKEN_EXPIRE_IN = 0.5


CONFIG = {
    "SECRET_KEY": SECRET_KEY,
    "SQLALCHEMY_DATABASE_URI": 'sqlite:///db.sqlite'
}


TEST_CONFIG = {
    "SECRET_KEY": SECRET_KEY,
    "SQLALCHEMY_DATABASE_URI": 'sqlite:///test_db.sqlite'
}

