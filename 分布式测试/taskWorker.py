"""
@author:jansonlv
@file: taskWorker.py
@time: 2016/7/15
@IDE: PyCharm
@project:distribute
"""

import time
from multiprocessing.managers import BaseManager

# 获取接口
class QueueManager(BaseManager):
    pass

# 注册获取
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 定义ip和端口
server_addr = ('192.168.10.128', 8001)

print('connect to server {}'.format(str(server_addr)))

# 绑定并实例化对象
m = QueueManager(server_addr, 'janson'.encode())

# 连接
m.connect()

# 获取queue对象
task = m.get_task_queue()
result = m.get_result_queue()

# 获取的任务不为空时
while not task.empty():
    image_url = task.get(True, timeout=5)
    print('run task download {}'.format(image_url))
    result.put('{}------>success'.format(image_url))

print('worker exit!')





