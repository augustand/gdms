# encoding=utf-8

# 这个是代理模块,他将处理模型层与表单以及展示层之间的逻辑关系
# 模型层只做对数据库的存取,其他的像加密,比较什么的都不做,表单只做验证,对数据格式内容校验,
# 和数据库分离开,它不做数据库的任何东西,当然加密解密也和他没什么关系,表单的返回结果只有true或则false
import sys

import os


class Proxy(object):

    def __init__(self):
        self.current_form = None
        self.current_model = None

    # 将表单转化为模型
    def to_model(self, model):
        for field_name, field in self.fields:
            if not field_name.startswith('validate_'):
                if field_name in dir(model):
                    setattr(
                        model, field_name, self.__getattribute__(field_name).data)
        return self

    # 得到表单
    def form_of(self, form_cls, form_data=None):
        forms = sys.modules['app.forms']
        cls = getattr(forms, 'LoginForm')
        print cls
        print cls()

        # Form = eval(form_cls)Form(form_data)
        return 'ok'

    # 得到表单
    def model_of(self, model_cls):
        Form = eval(model_cls)
        return Form
