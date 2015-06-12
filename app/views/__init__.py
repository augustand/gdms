# encoding=utf-8
from app import app
from flask import render_template
from .user import user
from ..forms import LoginForm


@app.route("/",methods=['GET'])
def index():
	return render_template("index.html")


app.register_blueprint(user,url_prefix='/user')


