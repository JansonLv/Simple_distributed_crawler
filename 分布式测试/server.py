""" 
@author:jansonlv
@file: server.py 
@time: 2016/7/15
@IDE: PyCharm
@project:distribute 
"""

import random
import time
import queue
from multiprocessing.managers import BaseManager

# 定义一个任务队列和结果队列
tack_queue = queue.Queue()
result_queue = queue.Queue()

# 定义一个继承BaseManaher的QueueManager获取QUeue接口添加任务
class QueueManager(BaseManager):
    pass

# 类将队列注册到网络上
QueueManager.register('get_task_queue', callable=lambda:tack_queue)
QueueManager.register('get_result_queue', callable=lambda:result_queue)

# 绑定ip和端口,并初始化对象产生实例,'janson'为验证口令
manager = QueueManager(('192.168.10.128', 8001), 'janson'.encode())

# 启动,开始监听
manager.start()

# 通过管理类的方法获取网络访问的queue对象
task = manager.get_task_queue()
result = manager.get_result_queue()

# 添加任务
for url in ["test_"+str(i) for i in range(10)]:
    print('put task {}'.format(url))
    task.put(url)

print('接收返回结果')

# 返回任务
for i in range(10):
    print('result is {}'.format(result.get(timeout=10)))

manager.shutdown()

