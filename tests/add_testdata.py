#!/usr/bin/env python3
import sys
sys.path.append('..')  # fix import directory

from app import db
from app.models import *

db.drop_all()
db.create_all()

dept_class = Department('教务处','综合教务系统')
dept_dorm = Department('后勤部门','热水工程设备')
dept_lib = Department('图书馆','图书馆')
dept_net = Department('网络中心','校园网络')

'''
class1 = Location('一教', dept_class)
class2 = Location('二教', dept_class)
class3 = Location('三教', dept_class)
class5 = Location('五教', dept_class)

dorm0 = Location('西区 #1', dept_dorm)
dorm1 = Location('东区 221', dept_dorm)

lib0 = Location('西区中文书库', dept_lib)
lib1 = Location('西区英文书库', dept_lib)
lib2 = Location('东区人文书库', dept_lib)
lib3 = Location('东区科技书库', dept_lib)
lib4 = Location('东区英才书院', dept_lib)

net0 = Location('有线网络', dept_net)
net1 = Location('ustcnet 无线', dept_net)
net2 = Location('网络通', dept_net)
net3 = Location('校园卡', dept_net)
net4 = Location('电子邮件', dept_net)
'''

manager_class = User('classadm', 'classadm', 'Manager', dept_class)
manager_dorm = User('dormadm', 'dormadm', 'Manager', dept_dorm)
manager_lib = User('libadm', 'libadm', 'Manager', dept_lib)
manager_net1 = User('netadm1', 'netadm1', 'Manager', dept_net)
manager_net2 = User('netadm2', 'netadm2', 'Manager', dept_net)

worker_net1 = User('worker1', 'worker1', 'Worker', dept_net)
worker_net2 = User('worker2', 'worker2', 'Worker', dept_net)
worker_net3 = User('worker3', 'worker3', 'Worker', dept_net)

ticket1 = Ticket()
ticket1.department = dept_net
ticket1.location = '有线网络'
ticket1.status = 'unassigned'
ticket1.description = '西区 #11 楼网络不稳定'
ticket1.reporter_email = 'boj@mail.ustc.edu.cn'
ticket1.reporter_phone = '0551-00000000'
ticket1.save()

ticket2 = Ticket()
ticket2.department = dept_net
ticket2.location = '网络通'
ticket2.status = 'assigned'
ticket2.description = '网络通密码忘了'
ticket2.reporter_email = 'boj@mail.ustc.edu.cn'
ticket2.reporter_phone = '0551-00000000'
ticket2.assign_time = datetime.utcnow()
ticket2.manager = manager_net1
ticket2.worker = worker_net1
ticket2.save()

ticket3 = Ticket()
ticket3.department = dept_net
ticket3.location = '网络通'
ticket3.status = 'closed'
ticket3.description = '网络通 7 号出口上不了 Facebook'
ticket3.reporter_email = 'boj@mail.ustc.edu.cn'
ticket3.reporter_phone = '0551-00000000'
ticket3.assign_time = datetime.utcnow()
ticket3.manager = manager_net2
ticket3.worker = worker_net2
ticket3.respond_time = datetime.utcnow()
ticket3.response = '不是本部门负责的问题'
ticket3.save()

