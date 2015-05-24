from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80),server_default='')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
                               backref=db.backref('posts', lazy='dynamic'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50))


@manager.command
def run():
    app.debug = True
    app.run()


if __name__ == '__main__':
    manager.run()

# test
# c1 = Category(password = 'pass1')
# p1 = Post(name='name1',category=c1)
# db.session.add(p1)
# db.session.commit()
#
# p1 = db.session.query(Category).one()
# print p1.id == 1
# print p1.posts.one().name == 'name1'
# print p1.posts.all()[0].name =='name1'
