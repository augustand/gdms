#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, prompt_bool
from app import app, db

import os

basedir = os.path.dirname(__file__)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    if prompt_bool("你想要删除数据库的所有数据吗？"):
        db.drop_all()


@manager.command
def init_env():
    os.system('make makefile')


@manager.command
def run():
    app.run()


if __name__ == "__main__":
    manager.run()
