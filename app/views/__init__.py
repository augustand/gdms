#encoding=utf-8
from app import app


@app.route('/')
def hello():
    return 'ok'


from .user import user
app.register_blueprint(user,url_prefix='/user')
