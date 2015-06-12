# encoding=utf-8

# 这是一个简单的后台验证框架,因为前台的话要用ajax处理,那么后台就不需要复杂的表单处理了


# 基础表单类,具体验证表单继承它
from flask import session


class BaseForm(object):
	def __init__(self,form=None):

		self.form = form
		self.fields = []
		self.errors = []  # 错误信息存放的地方
		self.init()

	def init(self):
		if not self.form:
			return False

		# 给表单赋值
		for field_name in dir(self):
			field = self.__getattribute__(field_name)
			if isinstance(field,Field):
				if self.form.has_key(field_name):
					field.data = self.form[field_name]
					self.fields.append((field_name,field.validate))

		# 验证自定义的以validate_开头的方法
		for validate_method in dir(self):
			if validate_method.startswith('validate_'):
				self.fields.append((validate_method,self.__getattribute__(validate_method)))


	# 验证入口
	def validate(self):
		status = True
		for field_name,validate_method in self.fields:
			status = validate_method() and status
			if not status:
				print field_name,status
				return False
		return status

# 字段类,主要提供字段的各种验证和约束
class Field(object):
	def __init__(self,label=None,type='text',validators={},description=None,data=''):
		self.data = data
		self.label = label
		self.type = type
		self.validators = validators
		self.description = description

	# 验证入口,验证该字段所有的约束条件
	def validate(self):
		status = True
		for method_name,param in self.validators.items():
			status = self.__getattribute__(method_name)(param) and status
			if not status:
				print method_name,status
				return True
		return status

	# 验证数据是否复合正则表达式
	def __rule(self,re_str):
		import re

		pattern = re.compile(re_str)
		match = pattern.match(self.data)
		if match:
			return True
		return False

	# 对开提供的正则表达式模块
	def regex(self,re_str):
		return self.__rule(re_str)

	# 是否为数字
	def digits(self,status=True):
		return self.__rule(r"\d+")

	# 是否是链接
	def url(self,status=True):
		re_str = r"^(https?|s?ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$"
		return self.__rule(re_str)

	# 是否是邮箱
	def email(self,status=True):
		re_str = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
		return self.__rule(re_str)

	# 是否为空
	def not_null(self,status):
		if not status:
			return True
		if not self.data:
			return False
		if hasattr(self.data,'replace') and len(self.data.replace(' ','')) < 0:
			return False
		if len(self.data) == 0:
			return False
		return True

	# 最小长度
	def min_length(self,min=-1):
		return self.not_null(True) and len(self.data) >= min

	# 长度范围
	def length_range(self,range=[]):
		if self.not_null(True) and len(range) == 2:
			data_length = len(self.data)
			return data_length >= range[0] and data_length <= range[1]
		return False

	# 最大长度
	def max_length(self,max):
		return self.not_null(True) and len(self.data) <= max

	# 最小值
	def min(self,min):
		try:
			return int(self.data) >= min
		except Exception,e:
			print e
			return False

	# 最大值
	def max(self,max):
		try:
			return int(self.data) <= max
		except Exception,e:
			print e
			return False

	# 值范围
	def data_range(self,range=[]):
		try:
			data = int(self.data)
			if len(range) == 2:
				return data >= range[0] and data <= range[1]
			return False
		except Exception,e:
			print e
			return False

	# 是否等于field
	def equal_to(self,field):
		return self.data == field.data

	# 是否为规定的值
	def choices(self,args=[]):
		return self.data in args

	# 检查多选框
	def checked(self,status=True):
		if not status:
			return True
		return self.data in [1,'y','yes','true']

