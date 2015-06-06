# encoding=utf-8

class A(object):
    def __init__(self):
        print "初始化a"

    def run(self):
        print "运行a"

class B(A):
    def __init__(self):
        print '开始初始化b'
        super(B, self).__init__()
        print '结束初始化b'

    def run(self):
        print "开始运行b"
        super(B, self).run()
        print '结束运行b'


class C(B):
    def __init__(self):
        print '开始初始化c'
        super(C, self).__init__()
        print '结束初始化c'

    def run(self):
        print "开始运行c"
        super(C, self).run()
        print '结束运行c'


if __name__ == '__main__':
    c = C()
    c.run()

# 结果是：
# 开始初始化c
# 开始初始化b
# 初始化a
# 结束初始化b
# 结束初始化c
# 开始运行c
# 开始运行b
# 运行a
# 结束运行b
# 结束运行c
# 从结果我们可以看出,super采取的是深度优先遍历继承
