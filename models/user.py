from . import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, pswd):
        self.password_hash = generate_password_hash(pswd)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        return user
