import os


class Config:
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or
        'sqlite:///database.sqlite'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = (
        os.environ.get('JWT_SECRET_KEY')
        or
        'some secret key to make JWT more secure'
    )


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True
