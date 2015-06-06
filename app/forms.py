# encoding=utf-8
from .models import Student

from .form import BaseForm,Field


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
		user = Student.get_user(self.username.data)
		if not user:
			self.errors.append(u'用户名错误')
			return False

		if user.password != self.password.data:
			self.errors.append(u'密码错误')
			return False
		return True
