# encoding=utf-8
from app import db
from flask import g
from sqlalchemy.orm import backref


class Teacher(db.Model):
    __tablename__ = 'teachers'

    '''老师数据库字段设计'''
    id = db.Column(db.BigInteger, primary_key=True)

    username = db.Column(
        db.String(64), unique=True, index=True, nullable=False)  # 老师的工号 workID
    password = db.Column(db.String(128), nullable=False)

    student_amount = db.Column(db.SMALLINT, default=0)  # 老师指导的学生数量

    is_active = db.Column(db.Boolean, default=True)  # 是否激活
    # auth = db.Column(db.String)  # 用户权限

    notice = db.Column(db.Text)
    attachment = db.Column(db.String(100))
    is_comment_teacher = db.Column(db.Boolean, default=True)

    comment_teacher = db.relationship("Teacher", backref=backref(
        "commented_teacher", remote_side=[id]), uselist=False)
    comment_teacher_id = db.Column(db.BigInteger, db.ForeignKey('teachers.id'))

    @staticmethod
    def get_user(username):
        try:
            user = Teacher.query.filter(Teacher.username == username).first()
            if not user:
                user = Teacher.query.filter(Teacher.id == username).first()
            g.user = user
            return user
        except Exception, e:
            print e
            return None


# class Comment(db.Model):
# __tablename__ = 'teachers'
# '''评阅老师和被评阅老师的映射'''
# 	id = db.Column(db.BigInteger,primary_key=True)
#
# 	teacher = db.relationship("Teacher",backref=backref("teacher"),uselist=False)
# 	comment_teacher_id = db.Column(db.BigInteger,db.ForeignKey('teachers.id'))


class Student(db.Model):
    __tablename__ = 'students'
    '''学生数据库字段设计'''
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(
        db.String(64), unique=True, index=True, nullable=False)  # studentID
    password = db.Column(db.String(128), nullable=False)

    student_name = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)  # 账户是否激活
    sex = db.Column(db.SMALLINT, default=0)
    attachment = db.Column(db.String(100))

    mark = db.Column(db.SMALLINT)  # 评阅老师对毕设打的分数

    comment = db.Column(db.Text)  # 老师对该毕设的评论

    grade = db.Column(db.String(20))

    @staticmethod
    def get_user(username):
        try:
            user = Student.query.filter(Student.username == username).first()
            if not user:
                user = Student.query.filter(Student.id == username).first()
            g.user = user
            return user
        except Exception, e:
            print e
            return None

    def save(self):
        db.session.add(self)
        db.session.commit()


class Task(db.Model):
    __tablename__ = 'tasks'
    '''老师发布的课题'''
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, default=u'课题的简介')
    attachment = db.Column(db.String(100), default=u'附件路径')

    teacher_id = db.Column(db.BigInteger, db.ForeignKey('teachers.id'))
    teacher = db.relationship("Teacher", backref="tasks")

    student_id = db.Column(db.BigInteger, db.ForeignKey('students.id'))
    student = db.relationship("Student", backref="tasks", uselist=False)


class Admin(db.Model):
    __tablename__ = 'admin'
    '''系统管理员'''
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(
        db.String(64), unique=True, index=True, nullable=False)  # workID
    password = db.Column(db.String(128), nullable=False)

    task_start_date = db.Column(db.Date)
    task_end_date = db.Column(db.Date)

    comment_start_date = db.Column(db.Date)
    comment_end_date = db.Column(db.Date)

    @staticmethod
    def get_user(username):
        try:
            user = Admin.query.filter(Admin.username == username).first()
            if not user:
                user = Admin.query.filter(Admin.id == username).first()
            g.user = user
            return user
        except Exception, e:
            print e
            return None
