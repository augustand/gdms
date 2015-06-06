# encoding=utf-8
from app.models import Student
from flask import g

import re
from flask.ext.wtf import Form
from wtforms import StringField, RadioField, PasswordField, TextAreaField, BooleanField, DateField, ValidationError, \
    IntegerField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo
from wtforms.widgets import ListWidget, HTMLString


class BSListWidget(ListWidget):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ""
        for subfield in field:
            html += u'<label class="radio-inline"> %s%s </label>' % (subfield(), subfield.label.text)
        return HTMLString(html)


class Fields(object):
    notnull = u'该项输入不能为空'

    def get_len_str(min=None, max=None):
        if min and not max:
            return u"该项输入的最小长度必须是%d" % min
        elif max and not min:
            return u"该项输入的最大长度必须是%d" % max
        else:
            return u'该输入的长度必须大于%d,小于%d' % (min, max)

    username = StringField(label=u'请输入您的用户名',
                           validators=[DataRequired(message=notnull),
                                       Length(min=0, max=15, message=get_len_str(0, 16)),
                                       ])

    password = PasswordField(label=u'请输入密码', description=u'请输入密码',
                             validators=[DataRequired(message=notnull),
                                         Length(min=0, max=60, message=get_len_str(min=0, max=61)),
                                         ])
    confirm_password = PasswordField(label=u'请确认密码',
                                     description=u'请确认密码',

                                     validators=[DataRequired(message=notnull),
                                                 Length(min=5, max=60, message=get_len_str(min=4, max=61)),
                                                 EqualTo(u'confirm_password', message=u'两次输入的密码不一致'), ]
                                     )
    student_amount = StringField(label=u'请输入您指导的学生数量',
                                 validators=[Regexp(re.compile(r"\d"))])

    is_active = RadioField(label=u'是否激活账户',
                           coerce=int,
                           choices=[(0, u'否'), (1, u'是')],
                           default=0,
                           widget=BSListWidget())

    notice = TextAreaField(label=u'请填写对学生的通知')

    attachment = StringField(label=u'添加附加',
                             validators=[Length(min=0, max=32, message=get_len_str(min=0, max=33))], )

    is_comment_teacher = RadioField(label=u'是否有评价功能',
                                    coerce=int,
                                    choices=[(0, u'否'), (1, u'是')],
                                    default=0,
                                    widget=BSListWidget())

    student_name = StringField(label=u'请输入您的姓名',
                               description='',
                               validators=[DataRequired(message=notnull),
                                           Length(min=0, max=15, message=get_len_str(0, 16)),
                                           ])

    sex = RadioField(label=u'您的性别',
                     coerce=int,
                     choices=[(0, u'男'), (1, u'女')],
                     default=0,
                     widget=BSListWidget())

    user_type = RadioField(label=u'您是',
                           coerce=str,
                           choices=[(u'student', u'学生'), (u'teacher', u'老师'), (u'admin', u'管理员')],
                           default=u'student',
                           widget=BSListWidget())

    mark = StringField(label=u'您的分数',
                       default=0,
                       validators=[DataRequired(message=notnull),
                                   Length(min=0, max=100, message=get_len_str(0, 101)),
                                   ])
    comment = TextAreaField(label=u'请填写您对学生的评语',
                            validators=[
                                Length(min=0, max=128, message=get_len_str(0, 129)),
                            ])

    title = StringField(label=u'请填写毕业设计的题目',
                        validators=[
                            Length(min=0, max=128, message=get_len_str(0, 129)),
                        ])
    description = TextAreaField(label=u'请填写毕业设计的描述')

    task_start_date = DateField(label=u'开始时间')
    task_end_date = DateField(label=u'结束时间')

    comment_start_date = DateField(label=u'开始时间')
    comment_end_date = DateField(label=u'结束时间')


class LoginForm(Form):
    username = Fields.username
    password = Fields.password

    user_type = Fields.user_type

    remember_me = BooleanField(label=u'记住我', default=u'y')

    errors = {}


    def validate_fields(self):
        status = True
        status = status and self.username.validate(self)
        status = status and self.username.validate(self)
        self.password.validate()

        # def validate(self):
        self._fields
        self.validate_on_submit()
        return self.username.validate(self)

        # def validate_username(self, field):
        # user = Student.get_user(field.data)
        # if not user:
        # print 'not user'
        # self.errors['username'] = u'用户名不存在'
        # raise ValidationError(message=u'该用户名已被注册')
        # else:
        # print 'user'
        # return True

        #
        # def validate_password(self,field):
        # if g.user:
        # if field.data != g.user.username:
        # field.errors.append(message=u'用户密码不正确')
        # return False
        #
        # def validate_user_type(self, field):
        # print field.data
        #
        # def validate_remember_me(self,field):
        # if field.data:
        # print field.data


class StuInfo(Form):
    username = Fields.username
    student_name = Fields.student_name
    sex = Fields.sex
    attachment = Fields.attachment
    mark = Fields.mark
    comment = Fields.comment


