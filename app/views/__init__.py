#encoding=utf-8
from app import app
from app.forms import LoginForm
from flask import render_template, request,redirect
from .user import user

@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm(request.form)
    print form.username.data
    if request.method == "POST" and form.validate():
            print form.username.data
            return redirect("/")
    print form.username.data
    return render_template("index.html", form=form)


app.register_blueprint(user,url_prefix='/user')
