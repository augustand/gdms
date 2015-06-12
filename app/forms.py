# encoding=utf-8
from flask import g,session
from .models import Student,Teacher,Admin

from .form import BaseForm,Field
from .proxy import Proxy
proxy = Proxy()

# 用户登录表单
class LoginForm(BaseForm):
	username = Field(label=u'请输入用户名:',
		description=u'用户名不能为空,长度在3到10之间',
		validators={'not_null':True,'length_range':[3,15]}
	)

	password = Field(label=u'请输入密码',
		description=u'密码不能为空,长度在3到15之间',
		validators={'not_null':True,'length_range':[3,15]}
	)

	user_type = Field(label=u'您是:',
		description=u'用户类型是学生,老师,管理员',
		validators={'not_null':True,'choices':['student','teacher','admin']}
	)

	remember_me = Field(label=u'记住我',
		validators={"checked":True},
		description=u'记住我方便下次登录'
	)

	def validate_login(self):
		if not self.user_type.data:
			self.errors.append(u'用户类型不存在')
			return False

		user_type = self.user_type.data
		username = self.username.data
		if user_type == 'student':
			user = Student.get_user(username)
		elif user_type == 'teacher':
			user = Teacher.get_user(username)
		elif user_type == 'admin':
			user = Admin.get_user(username)
		else:
			return False

		if not user:
			self.errors.append(u'用户名错误')
			return False

		if user.password != self.password.data:
			self.errors.append(u'密码错误')
			return False

		session['username'] = user.username
		session['user_type'] = user_type
		return True


# 用户信息表单
class StuInfoForm(BaseForm):
	username = Field(label=u'学号:')
	student_name = Field(label=u'姓名')
	sex = Field(label=u'性别')
	mark = Field(label=u'分数')
	comment = Field(label=u'老师评语')
	grade = Field(label=u'班级')

	password = Field(label=u'密码')

	attachment = Field(label=u'附件')

	def get_user(self,username):
		return Student.get_user(username)

	def save(self):
		user = self.get_user(session['username'])
		user = self.to_model(user)
		user.save()


# 教师注册表单

class TeacherForm(BaseForm):
	pass

# username
# password
# student_amount
# notice
# attachment
