""" 
@author:jansonlv
@file: DataOutpt.py 
@time: 2017/10/25 
@IDE: PyCharm
@project:Simple_distributed_crawler 
"""

import codecs
import time

class DataOutpt(object):
    def __init__(self):
        self.filepath= 'baike_{}.html'.format(time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime()))

        self.data = []