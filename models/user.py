from . import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, pswd):
        self.password_hash = generate_password_hash(pswd)

    def save(self):
        db.session.add(self)
        db.session.commit()
