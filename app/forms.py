import re
from flask.ext.wtf import Form
from wtforms import StringField, RadioField, PasswordField, TextAreaField, BooleanField, DateField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo
from wtforms.widgets import ListWidget, HTMLString


class BSListWidget(ListWidget):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = []
        for subfield in field:
            html.append(u'<label class="radio inline"> %s%s </label>' % (subfield(), subfield.label.text))
        return HTMLString(u''.join(html))


class Fields(object):
    notnull = u'该项输入不能为空'

    def get_len_str(min=None, max=None):
        if min and not max:
            return u"该项输入的最小长度必须是%d" % min
        elif max and not min:
            return u"该项输入的最大长度必须是%d" % max
        else:
            return u'该输入的长度必须大于%d,小于%d' % (min, max)

    workID = StringField(label=u'请输入您的工号', validators=[DataRequired(message=notnull),
                                                       Length(min=5, max=10, message=get_len_str(4, 11)),
                                                       ])

    password = PasswordField(label=u'请输入密码',
                             validators=[DataRequired(message=notnull),
                                         Length(min=5, max=60, message=get_len_str(min=4, max=61)),
                                         EqualTo(u'confirm_password', message=u'两次输入的密码不一致'), ],
                             description=u'请输入密码'
                             )
    confirm_password = PasswordField(label=u'请确认密码',
                                     description=u'请确认密码',

                                     validators=[DataRequired(message=notnull),
                                                 Length(min=5, max=60, message=get_len_str(min=4, max=61)), ]
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

    studentID = StringField(label=u'请输入您的学号',
                            validators=[DataRequired(message=notnull),
                                        Length(min=0, max=15, message=get_len_str(0, 16)),
                                        ])

    student_name = StringField(label=u'请输入您的姓名',
                               validators=[DataRequired(message=notnull),
                                           Length(min=0, max=15, message=get_len_str(0, 16)),
                                           ])

    sex = RadioField(label=u'您的性别',
                     coerce=int,
                     choices=[(0, u'男'), (1, u'女')],
                     default=0,
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

    task_start_date = DateField(label='开始时间',default=)




    email = StringField(label=u'请输入邮箱',
                        validators=[DataRequired(message=notnull), Email(message=u'邮箱格式不正确')],
                        description=u'请输入邮箱'
                        )

    sex = RadioField(label=u'请选择您的性别',
                     coerce=int,
                     choices=[(0, u'男'), (1, u'女'), (2, u'不确定')],
                     default=2,
                     description=u'请选择您的性别',
                     widget=BSListWidget()
                     )

    nickname = StringField(label=u"请输入您的昵称",
                           validators=[Length(min=3, max=32, message=get_len_str(min=2, max=33))],
                           description=u'请输入您的昵称',
                           default=u'我没有昵称'
                           )

    about_me = TextAreaField(label=u'请描述一下自己吧',
                             validators=[Length(min=15, max=128, message=get_len_str(min=14, max=129))])

    remember_me = BooleanField(label=u'记住我', default=0)

    birthday = DateField(label=u'请选择您的生日', default=date.today())
    born_place = StringField(label=u'所在地', default=u'地球上')

    signature = StringField(label=u'请填写您的签名',
                            validators=[Length(max=64, message=get_len_str(min=None, max=64))],
                            )

    @staticmethod
    def validate_email(form, field):
        user = User.get_user(field.data)
        if user:
            raise ValidationError(message=u'该email已被注册')


class StuRegForm(Form):
    studentID = Fields.username
    email = Fields.email
    sex = Fields.sex
    password = Fields.password
    confirm_pdbassword = Fields.confirm_password

    def validate_username(self, field):
        name = field.data
        if name.lower() in RESERVED_WORLDS:
            # self.username.errors.append(u'该用户名为系统保留字')
            raise ValidationError(message=u'该用户名为系统保留字')
        user = User.get_user(name)
        if user:
            raise ValidationError(message=u'该用户名已被注册')

    def validate_email(self, field):
        Fields.validate_email(self, field)

    def save(self):
        try:
            user = User()
            self.populate_obj(user)
            return user.save()
        except:
            return None
