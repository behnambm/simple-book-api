from flask_script import Manager
from models import db
from models.user import User
from app import app
from tqdm import tqdm

manager = Manager(app)


@manager.command
def init_db():
    db.create_all()

    user_list = [
        {
            'first_name': 'Ben',
            'last_name': 'blake',
            'email': 'ben_blake@email.com'
        },
        {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john_smith@email.com'
        },
        {
            'first_name': 'hugo',
            'last_name': 'alfred',
            'email': 'hugo_alfred@email.com'
        },
    ]
    for user in tqdm(user_list):
        'This is only for populating database.'
        tmp_user = User(
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
            password='123'
        )
        tmp_user.save()

    print('Database successfully initialized.')


if __name__ == '__main__':
    manager.run()
