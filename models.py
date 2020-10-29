from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')
    books = db.relationship('Book', lazy='dynamic', backref='author', cascade='all,delete')

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

    def add_role(self, role_name=None):
        if role_name:
            role = Role.get_role_by_name(role_name)
            if role:
                _user_role = UserRoles(user_id=self.id, role_id=role.id)
                db.session.add(_user_role)
                db.session.commit()

    def has_role(self, name):
        roles = [role.name for role in self.roles]
        return name in roles


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    @classmethod
    def get_role_by_name(cls, name=None):
        return cls.query.filter_by(name=name).first()


# association table for user roles
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')) # noqa
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE')) # noqa


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    publish_date = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def get_book_by_id(cls, book_id):
        return cls.query.filter_by(id=book_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
