# encoding=utf-8
from app import db
from app.models import Student, Teacher
from flask import request, Blueprint, redirect, render_template, g, flash, jsonify, session, url_for, current_app, \
    send_from_directory
from ..forms import LoginForm, StuInfoForm
import os
from werkzeug.utils import secure_filename
from ..proxy import Proxy

user = Blueprint('user', __name__, template_folder='user')
proxy = Proxy()


@user.route('/login', methods=['POST'])
def login_validate():
    # form = LoginForm(request.form)
    # form.validate()
    form = proxy.form_of('LoginForm', request.form)
    if form.validate():
        return jsonify(value='true')
    else:
        flash(u"登录失败", category='error')
        return jsonify(value='false', errors=form.errors)


@user.route('/logout', methods=['GET'])
def logout():
    if session.has_key('username'):
        del session['username']
        g.user = None
    return redirect('/')


@user.route('/info/', methods=['GET'])
def info():
    if session.has_key('username'):
        username = session['username']
        user_type = session['user_type']
        if user_type == 'student':
            user = Student.get_user(session['username'])
            file_dir = os.path.join(
                current_app.config['UPLOAD_FOLDER'], username + '/gd/')
            all_files = os.listdir(file_dir)
            return render_template("includes/index/info.html", user=user, filenames=all_files)
        elif user_type == 'admin':
            pass
        else:
            pass

    return "please login"


@user.route('/upload', methods=['POST'])
def upload():
    file = request.files['attachment']
    if file:
        filename = secure_filename(file.filename)
        file_dir = os.path.join(
            current_app.config['UPLOAD_FOLDER'], session['username'] + '/gd/')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file.save(os.path.join(file_dir, filename))
    return redirect('/user/info')


@user.route('/uploads/<path:filename>')
def download_file(filename):
    if session.has_key('username'):
        file_dir = os.path.join(
            current_app.config['UPLOAD_FOLDER'], session['username'] + '/gd/')
        return send_from_directory(file_dir, filename, as_attachment=True)
    return '请登录'


@user.route('/edit', methods=['POST'])
def edit():
    form = StuInfoForm(request.form)
    if form.validate():
        form.save()
    return redirect('/user/info')


@user.route('/changepass', methods=['POST'])
def change_pass():
    old_password = request.form['old_password']
    password = request.form['password']

    user = Student.get_user(session['username'])
    if user and user.password == old_password:
        user.password = password
        db.session.add(user)
        db.session.commit()
        return redirect('/user/info')
    return '密码更改错误'


@user.route('/teacher_save', methods=['GET'])
def teacher_save():
    try:
        t = Teacher()
        t.id = 1
        t.username = '123455'
        t.password = 'aaaaaa'
        db.session.add(t)
        db.session.commit()
    except Exception, e:
        print e
    return 'ok'
