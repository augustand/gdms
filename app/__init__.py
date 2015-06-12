# coding:utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from gdms import config
#from flask.ext.admin import Admin

app = Flask(__name__)

# 初始化app的配置
config.init_app(app)

# 解决运行app时，current_app出错的问题
# 先将 App 的 App Context 推入栈中，使栈顶不为空
# ==>
ctx = app.app_context()
ctx.push()
# <==

#admin = Admin(app)

# 初始化数据库配置
db = SQLAlchemy(app)
print 'init db'

from . import models, views  # 这个不导入，没办法生成数据库
print 'import db'
