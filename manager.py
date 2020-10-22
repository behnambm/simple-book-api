from flask_script import Manager
from models import db
from models.user import User
from app import app
from tqdm import trange

manager = Manager(app)


@manager.command
def init_db():
    db.create_all()

    for i in trange(1, 4):
        'This is only for populating database.'

        tmp_user = User(
            username='test_user_{}'.format(i),
            email='test_mail_{}@email.com'.format(i),
            password='123'
        )
        tmp_user.save()

    print('Database successfully initialized.')


if __name__ == '__main__':
    manager.run()
