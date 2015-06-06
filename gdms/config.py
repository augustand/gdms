# -*- coding: utf-8 -*-


class Config(object):
    import os

    basedir = os.path.dirname(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = "postgresql://bergus:zhaojie521@localhost/bergus"
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db')

    CSRF_ENABLED = True
    SECRET_KEY = 'HappinessChargePrecure'

    # 管理员列表
    ADMINS = ['anytjf@live.com']

    # 语言
    LANGUAGES = {
        'cn': '中文（简体）',
        'ja': '日本語',
        'en': 'English'
    }

    # 调试模式
    DEBUG = True

    # 测试模式
    TESTING = True

    SECRET_KEY = 'you-will-never-guess'
    PER_PAGE = 10
    LINK_SIZE = ''
    CSS_FRAMEWORK = 'bootstrap3'


def init_app(app):
    app.config.from_object(Config)
    print 'init config'
