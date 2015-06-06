# encoding=utf-8

class Form(object):
    count = 0

    def __init__(self):
        self.name = 'name'

    def sayHi(self):  # 实例方法，sayHi指向这个方法对象，使用类或实例.sayHi访问
        print self.name, 'says Hi!'  # 访问名为name的字段，使用实例.name访问s
        print self.__dict__
        print self.count


a = Form()
print a.count
print Form.count
print Form.__dict__
print a.__dict__
print a.__class__.__dict__

print Form.sayHi
print a.sayHi
print dir(a)  # 获取实例的属性名，以列表形式返回

if hasattr(a, 'name'):  # 检查实例是否有这个属性
    setattr(a, 'name', 'tiger')  # same as: a.name = 'tiger'
print getattr(a, 'name')  # same as: print a.name

getattr(a, 'sayHi')()  # same as: cat.sayHi()

print Form.__base__.__name__
print Form.__bases__
print a.__class__
print Form
print Form.__flags__


# 是否为规定内的值
def select_from(self,*args):
	return 3 in args
