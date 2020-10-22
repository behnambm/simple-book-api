import os


class Config:
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or
        'sqlite:///database.sqlite'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True
