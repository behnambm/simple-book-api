from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

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

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)


# association table for user roles
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')) # noqa
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE')) # noqa
