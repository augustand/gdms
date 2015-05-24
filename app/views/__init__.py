#encoding=utf-8
from app import app


@app.route('/')
def hello():
    return 'ok'
