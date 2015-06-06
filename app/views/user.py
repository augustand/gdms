# encoding=utf-8
from flask import request,Blueprint,redirect,render_template,g,flash,jsonify,session
from ..forms import LoginForm

user = Blueprint('user',__name__,template_folder='user')


# @user.route("/login", methods=['GET', 'POST'])
# def login():
# print request.form
# form = LoginForm(request.form)
# print form.validate()
#     if request.method == "POST" and form.validate():
#         print 'oookk'
#         return 'ok'
#         # return redirect("/user/login")
#     return render_template("user/login.html", form=form)
#
#
# @user.route('/logout', methods=['GET', 'POST'])
# def logout():
#     g.user = None
#     return redirect("/")
#
#
# @user.route('/validate_username', methods=["GET", 'POST'])
# def validate_username():
#     print request.form
#     if request.form.get('username', 0) == '123':
#         return jsonify(value='true', msg=u'成功')
#     return jsonify(value='false', msg=u'失败')
#
#
# @user.route('/info', methods=['GET'])
# def info():
#     form = StuInfo(request.form)
#     if g.user:
#         form.password.data = g.user.password
#         form.username.data = g.user.username
#         form.sex.data = g.user.sex
#         form.attachment.data = g.user.attachment
#         form.mark.data = g.user.mark
#         form.comment.data = g.user.comment
#         form.student_name.data = g.user.student_name
#     else:
#         flash(u'请登录')
#         redirect('/')
#     return render_template("user/info.html", form=form)


@user.route('/login',methods=['POST'])
def login_validate():
	form = LoginForm(request.form)
	if form.validate():
		flash(u"登录成功",category='success')
		session['username'] = g.user.username
		return jsonify(value='true')
	else:
		return jsonify(value='false',errors=form.errors)


@user.route('/logout',methods=['GET'])
def logout():
	if session.has_key('username'):
		del session['username']
		g.user=None
	return redirect('/')

