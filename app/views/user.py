from app.forms import LoginForm
from flask import request, Blueprint,redirect, render_template


user = Blueprint('user', __name__, template_folder='user')

@user.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    print form.username.data
    if request.method == "POST" and form.validate():
            print form.username.data
            return redirect("/")
    print form.username.data
    return render_template("user/login.html", form=form)
